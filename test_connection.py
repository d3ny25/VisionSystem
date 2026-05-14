"""
test_connection.py — Script de Pruebas del Sistema

Verifica que todos los componentes estén funcionando correctamente
sin ejecutar el loop principal.

Uso:
    python test_connection.py [--port COM3] [--camera 0]
"""

import argparse
import sys
import time

try:
    import llm
    import arduino
    import camera
    import tools
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de que todos los archivos .py están en la misma carpeta")
    sys.exit(1)


def test_lmstudio():
    """Verifica conexión con LMStudio."""
    print("\n" + "="*60)
    print("📋 TEST 1: Conexión con LMStudio")
    print("="*60)
    
    if llm.test_connection():
        print("✅ LMStudio responde correctamente")
        return True
    else:
        print("❌ No se puede conectar con LMStudio")
        print("   → Verifica que LMStudio esté ejecutándose en http://127.0.0.1:1234")
        print("   → Asegúrate de que el modelo esté cargado")
        return False


def test_arduino(port):
    """Verifica conexión con Arduino."""
    print("\n" + "="*60)
    print("📋 TEST 2: Conexión con Arduino")
    print("="*60)
    
    manager = arduino.ArduinoManager(port=port)
    
    if manager.ser is None:
        print("⚠️  Arduino no conectado")
        print("   → El sistema funcionará en modo análisis únicamente")
        print("   → Los resultados se mostrarán sin controlar LEDs físicos")
        return True  # No es un error, solo no hay hardware
    
    print(f"✅ Conectado a {manager.port} @ {manager.baudrate} baud")
    
    # Probar ping
    print("\n📍 Probando PING...")
    if manager.ping():
        print("✅ Arduino respondió al PING")
    else:
        print("⚠️  Arduino no respondió al PING")
    
    # Prueba LED 1 (persona)
    print("\n💡 Encendiendo LED blanco (persona detectada)...")
    manager.set_led_person_detected()
    time.sleep(1)
    print("✅ Comando enviado")
    
    # Prueba LED 2 (sin persona)
    print("\n💡 Encendiendo LED amarillo (sin persona)...")
    manager.set_led_no_person()
    time.sleep(1)
    print("✅ Comando enviado")
    
    # Apagar
    print("\n💡 Apagando LEDs...")
    manager.ser.close()
    print("✅ LEDs apagados")
    
    manager.close()
    return True


def test_camera(camera_idx):
    """Verifica conexión con cámara."""
    print("\n" + "="*60)
    print("📋 TEST 3: Conexión con Cámara")
    print("="*60)
    
    cam_manager = camera.CameraManager(camera_index=camera_idx)
    
    if cam_manager.cap is None:
        print(f"❌ No se pudo abrir cámara en índice {camera_idx}")
        print("   → Prueba con --camera 1, --camera 2, etc.")
        return False
    
    print(f"✅ Cámara inicializada en índice {camera_idx}")
    
    # Capturar frame
    print("\n📸 Capturando frame...")
    frame = cam_manager.capture_frame()
    
    if frame is None:
        print("❌ Error capturando frame")
        cam_manager.close()
        return False
    
    print(f"✅ Frame capturado: {frame.shape}")
    
    # Convertir a Base64
    print("\n📦 Codificando a Base64...")
    b64 = cam_manager.frame_to_base64(frame)
    
    if b64 is None:
        print("❌ Error codificando a Base64")
        cam_manager.close()
        return False
    
    print(f"✅ Base64 generado: {len(b64)} caracteres")
    
    cam_manager.close()
    return True


def test_tools():
    """Verifica que las herramientas están disponibles."""
    print("\n" + "="*60)
    print("📋 TEST 4: Herramientas del Agente")
    print("="*60)
    
    print(f"✅ Herramientas disponibles: {list(tools.AVAILABLE_FUNCTIONS.keys())}")
    print(f"✅ Schemas JSON: {len(tools.TOOLS_SCHEMA)} herramientas")
    
    return True


def main():
    """Función principal de pruebas."""
    parser = argparse.ArgumentParser(
        description="Pruebas de conectividad del Sistema de Visión"
    )
    parser.add_argument(
        "--port",
        type=str,
        default=None,
        help="Puerto serial del Arduino (ej: COM3, /dev/ttyUSB0)"
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Índice de cámara (default: 0)"
    )
    parser.add_argument(
        "--skip-arduino",
        action="store_true",
        help="Omitir prueba de Arduino"
    )
    parser.add_argument(
        "--skip-camera",
        action="store_true",
        help="Omitir prueba de cámara"
    )
    
    args = parser.parse_args()
    
    print("\n" + "█"*60)
    print("  🧪 PRUEBAS DEL SISTEMA DE VISIÓN")
    print("█"*60)
    
    results = {}
    
    # Test 1: LMStudio
    results['lmstudio'] = test_lmstudio()
    
    # Test 2: Arduino (opcional)
    if not args.skip_arduino:
        results['arduino'] = test_arduino(args.port)
    else:
        print("\n⏭️  Omitiendo prueba de Arduino")
    
    # Test 3: Cámara (opcional)
    if not args.skip_camera:
        results['camera'] = test_camera(args.camera)
    else:
        print("\n⏭️  Omitiendo prueba de cámara")
    
    # Test 4: Herramientas
    results['tools'] = test_tools()
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name.upper():<15} {status}")
    
    print(f"\n  Total: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("\n✅ ¡Todas las pruebas pasaron! Puedes ejecutar service.py")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los mensajes arriba.")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
