"""
config.py — Configuración Centralizada

Almacena todas las constantes de configuración del sistema en un único lugar.
Facilita cambios sin modificar el código de los módulos.
"""

# ============================================================================
# CONFIGURACIÓN DE LMSTUDIO
# ============================================================================

LM_STUDIO_HOST = "127.0.0.1"
LM_STUDIO_PORT = 1234
LM_STUDIO_API_URL = f"http://{LM_STUDIO_HOST}:{LM_STUDIO_PORT}/v1/chat/completions"
LM_STUDIO_MODEL = "qwen/qwen3-vl-4b"
LM_STUDIO_API_KEY = "sk-lm-aRiEz0zg:CwVZ1egWOiLzZh50VBWe"
LM_STUDIO_TIMEOUT = 30  # segundos

# Parámetros de inferencia
LM_TEMPERATURE = 0.3      # Más determinístico para detección
LM_MAX_TOKENS = 256
LM_MAX_ITERATIONS = 5     # Máximas iteraciones del loop agéntico

# ============================================================================
# CONFIGURACIÓN DE ARDUINO
# ============================================================================

ARDUINO_BAUDRATE = 9600
ARDUINO_TIMEOUT = 1       # segundos
ARDUINO_AUTO_DETECT = True  # Buscar puerto automáticamente

# Comandos serial
CMD_PING = "PING"
CMD_PERSON_DETECTED = "1"
CMD_NO_PERSON = "0"
CMD_DISTANCE = "DISTANCE"

# Umbral y frecuencia del sensor ultrasónico
ULTRASONIC_THRESHOLD_CM = 120  # Distancia máxima para activar análisis
ULTRASONIC_POLL_INTERVAL = 0.5  # Segundos entre lecturas cuando está en IDLE

# ============================================================================
# CONFIGURACIÓN DE CÁMARA
# ============================================================================

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30
CAMERA_WARMUP_FRAMES = 5
CAMERA_MAX_SIZE = 384     # Redimensionar a máximo 384x384 para LLM
CAMERA_JPEG_QUALITY = 75  # Calidad de compresión JPEG

# ============================================================================
# CONFIGURACIÓN DE APLICACIÓN
# ============================================================================

APP_NAME = "Vision System - Detección de Personas"
APP_VERSION = "1.0.0"

# Delay entre ciclos de detección (segundos)
CYCLE_DELAY = 1.0

# Mostrar mensajes de debug
DEBUG = True
