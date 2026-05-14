"""
arduino.py — Módulo de Comunicación Serial con Arduino

Gestiona la conexión serial con el Arduino. La conexión es persistente 
(se abre una sola vez y se reutiliza), thread-safe (con threading.Lock) 
y auto-reconectable (si el puerto se cierra, el siguiente comando lo reabre).

Protocolo Serial (9600 baud):
- Envía '1' para encender LED blanco (persona detectada)
- Envía '0' para encender LED amarillo (sin persona)
"""

import serial
import threading
import time
import platform
import glob
from typing import Optional


class ArduinoManager:
    """Gestor de conexión serial persistente con Arduino."""
    
    def __init__(self, port: Optional[str] = None, baudrate: int = 9600, timeout: int = 1):
        """
        Inicializa el gestor de Arduino.
        
        Args:
            port: Puerto serial (ej: COM3, /dev/ttyUSB0). Si es None, auto-detecta.
            baudrate: Velocidad de comunicación (9600 por defecto)
            timeout: Timeout de lectura en segundos
        """
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.lock = threading.Lock()
        self.port = port or self._find_port()
        
        if self.port:
            self._connect()
    
    def _find_port(self) -> Optional[str]:
        """Auto-detecta puerto Arduino disponible."""
        system = platform.system()
        
        try:
            if system == "Linux":
                # Buscar puertos USB y ACM en Linux
                ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
            elif system == "Windows":
                # Buscar puertos COM en Windows
                ports = [f"COM{i}" for i in range(1, 13)]
                ports = [p for p in ports if _port_exists(p)]
            elif system == "Darwin":  # macOS
                ports = glob.glob("/dev/tty.usbserial*") + glob.glob("/dev/tty.usbmodem*")
            else:
                ports = []
            
            if ports:
                print(f"✅ Puertos encontrados: {ports}")
                return ports[0]  # Usar el primer puerto encontrado
        except Exception as e:
            print(f"⚠️ Error en auto-detección de puerto: {e}")
        
        return None
    
    def _connect(self):
        """Intenta establecer conexión con Arduino."""
        if not self.port:
            print("❌ No se encontró puerto serial")
            return
        
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)  # Esperar a que Arduino se reinicie
            self.ser.reset_input_buffer()  # Limpiar mensajes de arranque
            print(f"✅ Arduino conectado en {self.port} ({self.baudrate} baud)")
        except serial.SerialException as e:
            print(f"❌ Error conectando Arduino: {e}")
            self.ser = None
    
    def _ensure_connected(self):
        """Verifica y reconecta si es necesario."""
        if self.ser is None or not self.ser.is_open:
            print("🔄 Reconectando Arduino...")
            self._connect()
    
    def send_command(self, command: str, wait_response: bool = True) -> Optional[str]:
        """
        Envía comando por serial y espera respuesta.
        
        Args:
            command: Comando a enviar (se agrega \\n automáticamente)
            wait_response: Si esperar respuesta de Arduino
        
        Returns:
            Respuesta de Arduino o None si falla
        """
        with self.lock:
            self._ensure_connected()
            
            if self.ser is None:
                print(f"❌ No hay conexión serial disponible")
                return None
            
            try:
                # Limpiar buffer antes de enviar
                self.ser.reset_input_buffer()
                
                # Enviar comando
                self.ser.write(f"{command}\n".encode())
                
                if wait_response:
                    while True:
                        response = self.ser.readline().decode().strip()
                        if response == "" or response == "READY":
                            continue
                        return response
                
                return "OK"
            except Exception as e:
                print(f"❌ Error enviando comando: {e}")
                self.ser = None
                return None
    
    def set_led_person_detected(self) -> bool:
        """Enciende LED blanco (persona detectada)."""
        response = self.send_command('1')
        return response is not None
    
    def set_led_no_person(self) -> bool:
        """Enciende LED amarillo (sin persona)."""
        response = self.send_command('0')
        return response is not None
    
    def get_distance(self) -> Optional[float]:
        """Solicita la lectura de distancia del sensor ultrasónico al Arduino."""
        response = self.send_command('DISTANCE')
        if response is None:
            print("❌ No se recibió respuesta para DISTANCE")
            return None
        print(f"DEBUG: Raw DISTANCE response: {response}")
        if response.startswith("DISTANCE:"):
            payload = response.split(':', 1)[1].strip()
            if payload.upper() == "ERROR":
                return float('inf')
            try:
                return float(payload)
            except ValueError:
                print(f"❌ Respuesta de distancia inválida: {payload}")
                return None
        # Si la respuesta no tiene el formato esperado, reportar fallo
        print(f"❌ Respuesta de distancia inválida: {response}")
        return None
    
    def ping(self) -> bool:
        """Verifica que Arduino está conectado."""
        response = self.send_command('PING')
        return response == 'PONG'
    
    def close(self):
        """Cierra la conexión serial limpiamente."""
        with self.lock:
            if self.ser is not None:
                self.ser.close()
                self.ser = None
                print("🔌 Conexión Arduino cerrada")


def _port_exists(port: str) -> bool:
    """Verifica si un puerto COM existe en Windows."""
    try:
        s = serial.Serial(port)
        s.close()
        return True
    except:
        return False
