"""
service.py — Punto de Entrada y Orquestador

Es el único archivo que se ejecuta directamente. Contiene el loop principal 
que coordina todos los módulos:

1. Verifica conexión con LMStudio
2. Captura imágenes de la cámara
3. Pasa imagen al agente de IA
4. Ejecuta tools (controla LEDs)
5. Repite en loop infinito

Uso:
    python service.py [--port COM3] [--camera 0]
"""

import signal
import sys
import time
import argparse
from datetime import datetime

import camera
import arduino
import llm
import tools
import config


# ============================================================================
# VARIABLES GLOBALES
# ============================================================================

camera_manager = None
arduino_manager = None
running = True


# ============================================================================
# MANEJADORES DE SEÑALES
# ============================================================================

def signal_handler(sig, frame):
    """Maneja Ctrl+C para cerrar limpiamente."""
    global running
    print("\n\n🛑 Interrumpido por el usuario (Ctrl+C)")
    running = False
    cleanup()
    sys.exit(0)


def cleanup():
    """Cierra recursos limpiamente."""
    global camera_manager, arduino_manager
    
    print("\n🧹 Limpiando recursos...")
    
    if camera_manager:
        camera_manager.close()
    
    if arduino_manager:
        arduino_manager.close()
    
    print("✅ Limpieza completada")


# ============================================================================
# FUNCIONES DE INTERFAZ
# ============================================================================

def print_header(port: str, camera_idx: int, arduino_connected: bool):
    """Imprime encabezado decorativo."""
    print("\n" + "="*70)
    print("  🎥 SISTEMA DE VISIÓN CON DETECCIÓN DE PERSONAS")
    print("     Arquitectura Modular v1.0")
    print("="*70)
    print(f"  Puerto Arduino  : {port}")
    print(f"  Estado Arduino  : {'✅ Conectado' if arduino_connected else '⚠️  No conectado'}")
    print(f"  Índice Cámara   : {camera_idx}")
    print(f"  Comunicación    : HTTP (requests)")
    print(f"  Modelo IA       : qwen/qwen3-vl-4b")
    print("="*70 + "\n")


def print_result_box(status: str):
    """Imprime resultado en cuadro estético."""
    if status.startswith("SUCCESS"):
        parts = status.split(":")
        action = parts[1] if len(parts) > 1 else "DETECTADO"
        has_hardware = len(parts) < 4 or parts[3] != "NO_HARDWARE"
        
        symbol = "👤" if action == "PERSON" else "⭕"
        color = "🟢" if action == "PERSON" else "🟡"
        
        if has_hardware:
            print(f"\n    {color} {symbol} {action}\n")
        else:
            print(f"\n    {color} {symbol} {action} (Sin Hardware)\n")
    elif status.startswith("CANCEL"):
        print(f"\n    🔴 ⚠️  ANÁLISIS CANCELADO\n")
    else:
        print(f"\n    ❌ {status}\n")


def _on_agent_message(role: str, content: str):
    """Callback para mensajes del agente en tiempo real."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if role == "tool":
        print(f"[{timestamp}] 🔧 {content}")
    else:
        print(f"[{timestamp}] 💭 {content}")


# ============================================================================
# LOOP PRINCIPAL
# ============================================================================

def detection_loop():
    """Loop infinito de detección y análisis."""
    global camera_manager, arduino_manager, running
    
    cycle = 0
    
    active = False
    
    while running:
        cycle += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        try:
            # ====================================================================
            # 0. MONITOREO DEL SENSOR ULTRASÓNICO
            # ====================================================================
            if arduino_manager and arduino_manager.ser is not None:
                distance = arduino_manager.get_distance()
                if distance is None:
                    print(f"[{timestamp}] ⚠️  No se pudo leer distancia del sensor")
                    time.sleep(config.ULTRASONIC_POLL_INTERVAL)
                    continue
                
                if distance == float('inf'):
                    print(f"[{timestamp}] 🌡️ DISTANCE:ERROR (sin retorno / fuera de rango)")
                else:
                    print(f"[{timestamp}] 🌡️ DISTANCE:{distance:.1f} cm")
                
                if distance <= config.ULTRASONIC_THRESHOLD_CM:
                    if not active:
                        print(f"[{timestamp}] 🟢 Objeto dentro del rango ({config.ULTRASONIC_THRESHOLD_CM} cm). Activando análisis...")
                        active = True
                else:
                    if active:
                        print(f"[{timestamp}] 🔴 Objeto fuera de rango. Volviendo a IDLE y deteniendo análisis.")
                        active = False
                        if arduino_manager:
                            arduino_manager.set_led_no_person()
                    print(f"[{timestamp}] 💤 IDLE: esperando objeto dentro del rango...")
                    time.sleep(config.ULTRASONIC_POLL_INTERVAL)
                    continue
            
            # ====================================================================
            # 1. CAPTURAR IMAGEN
            # ====================================================================
            print(f"\n[{timestamp}] 📷 Ciclo {cycle}: Capturando imagen...")
            image_b64 = camera_manager.get_camera_data()
            if image_b64 is None:
                print(f"[{timestamp}] ❌ Error capturando imagen")
                time.sleep(config.CYCLE_DELAY)
                continue
            
            print(f"[{timestamp}] ✅ Imagen capturada ({len(image_b64)} bytes)")
            
            # ====================================================================
            # 2. ANALIZAR CON IA
            # ====================================================================
            print(f"[{timestamp}] 🧠 Ciclo {cycle}: Analizando con IA...")
            result = llm.act_on_image(image_b64, on_message=_on_agent_message)
            
            # ====================================================================
            # 3. MOSTRAR RESULTADO
            # ====================================================================
            print(f"\n[{timestamp}] 📊 Resultado final: {result}")
            print_result_box(result)
            
            time.sleep(config.CYCLE_DELAY)
        
        except Exception as e:
            print(f"[{timestamp}] ❌ Error en ciclo: {e}")
            time.sleep(config.CYCLE_DELAY)


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

def main():
    """Función principal."""
    global camera_manager, arduino_manager
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(
        description="Sistema de Visión Artificial con Detección de Personas"
    )
    parser.add_argument(
        "--port",
        type=str,
        default=None,
        help="Puerto serial del Arduino (ej: COM3, /dev/ttyUSB0). Autodetecta si no se especifica."
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=1,
        help="Índice de la cámara preferida (default: 1 para USB, 0 para interna)"
    )
    
    args = parser.parse_args()
    
    # Registrar manejador de interrupciones
    signal.signal(signal.SIGINT, signal_handler)
    
    # ====================================================================
    # INICIALIZAR MÓDULOS
    # ====================================================================
    
    # 1. Verificar conexión con LMStudio
    print("🔍 Verificando conexión con LMStudio...")
    if not llm.test_connection():
        print("❌ No se puede conectar con LMStudio. Asegúrate de que esté ejecutándose en http://127.0.0.1:1234")
        return
    
    # 2. Inicializar Arduino
    print("🔌 Inicializando Arduino...")
    arduino_manager = arduino.ArduinoManager(port=args.port)
    arduino_connected = arduino_manager.ser is not None
    
    if arduino_manager.ser is None:
        print("⚠️  Arduino no conectado. El sistema funcionará en modo análisis únicamente.")
        print("   → Los resultados se mostrarán en pantalla sin controlar LEDs físicos.")
    else:
        # Verificar conexión con ping
        if arduino_manager.ping():
            print("✅ Arduino conectado y respondiendo")
        else:
            print("⚠️  Arduino conectado pero no responde al ping")
    
    # Inyectar gestor de Arduino en tools
    tools.set_arduino_manager(arduino_manager)
    
    # 3. Inicializar Cámara
    print("📷 Inicializando cámara...")
    camera_manager = camera.CameraManager(camera_index=args.camera, warmup_frames=5)
    if camera_manager.cap is None:
        print("❌ No se pudo abrir la cámara")
        if arduino_manager:
            arduino_manager.close()
        return
    
    # Imprimir encabezado
    print_header(args.port or "Auto-detect", args.camera, arduino_connected)
    
    # ====================================================================
    # INICIAR LOOP PRINCIPAL
    # ====================================================================
    
    print("\n🟢 Sistema iniciado. Presiona Ctrl+C para salir.")
    print("=" * 70)
    
    try:
        detection_loop()
    finally:
        cleanup()


if __name__ == "__main__":
    main()
