"""
ESTRUCTURA DEL PROYECTO - VisionSystem V3

╔═══════════════════════════════════════════════════════════════════════╗
║         SISTEMA DE DETECCIÓN DE PERSONAS CON IA LOCAL                ║
║               Arquitectura Modular Completa                           ║
╚═══════════════════════════════════════════════════════════════════════╝

📁 VisionSystem V3/
│
├─ 📄 service.py ............................ [PUNTO DE ENTRADA]
│  │  ├─ Función: main()
│  │  ├─ Función: detection_loop()
│  │  ├─ Función: signal_handler()
│  │  ├─ Función: cleanup()
│  │  └─ Función: print_result_box()
│  │
│  └─ Responsabilidades:
│     • Inicializar y coordinar todos los módulos
│     • Manejar argumentos de línea de comandos
│     • Orquestar el loop principal
│     • Manejar interrupciones gracefully (Ctrl+C)
│
├─ 📄 llm.py ................................ [AGENTE DE IA]
│  │  ├─ Clase: (funciones modulares)
│  │  ├─ Función: test_connection()
│  │  ├─ Función: act_on_image()
│  │  ├─ Función: _make_api_call()
│  │  └─ Constantes: API_URL, MODEL, SYSTEM_PROMPT
│  │
│  └─ Responsabilidades:
│     • Comunicación HTTP con LMStudio
│     • Gestión del loop agéntico (tool-calling)
│     • Parseo de respuestas JSON
│     • Ejecución iterativa de tools
│
├─ 📄 tools.py .............................. [HERRAMIENTAS]
│  │  ├─ Función: person_detected()
│  │  ├─ Función: no_person()
│  │  ├─ Función: cancel_analysis()
│  │  ├─ Función: execute_tool()
│  │  ├─ Función: set_arduino_manager()
│  │  ├─ Constante: TOOLS_SCHEMA (JSON para LLM)
│  │  └─ Dict: AVAILABLE_FUNCTIONS (dispatch)
│  │
│  └─ Responsabilidades:
│     • Implementación Python de todas las herramientas
│     • Schemas JSON (descripción para LLM)
│     • Dispatch dinámico de funciones
│     • Inyección de dependencias (Arduino)
│
├─ 📄 arduino.py ............................ [COMUNICACIÓN SERIAL]
│  │  ├─ Clase: ArduinoManager
│  │  │  ├─ __init__(port, baudrate, timeout)
│  │  │  ├─ _initialize_camera()
│  │  │  ├─ _connect()
│  │  │  ├─ _ensure_connected()
│  │  │  ├─ send_command(command, wait_response)
│  │  │  ├─ set_led_person_detected()
│  │  │  ├─ set_led_no_person()
│  │  │  ├─ ping()
│  │  │  └─ close()
│  │  │
│  │  ├─ Función: _find_port()
│  │  ├─ Función: _port_exists()
│  │  └─ Atributos: lock (thread-safety)
│  │
│  └─ Responsabilidades:
│     • Conexión persistente (abre 1 vez, reutiliza)
│     • Thread-safety con locks
│     • Auto-detección de puertos
│     • Auto-reconexión si se cierra
│     • Envío/recepción de comandos seriales
│
├─ 📄 camera.py ............................. [CAPTURA DE IMÁGENES]
│  │  ├─ Clase: CameraManager
│  │  │  ├─ __init__(camera_index, warmup_frames)
│  │  │  ├─ _initialize_camera()
│  │  │  ├─ capture_frame()
│  │  │  ├─ frame_to_base64(frame, max_size)
│  │  │  ├─ get_camera_data()
│  │  │  └─ close()
│  │  │
│  │  ├─ Atributos: lock (thread-safety)
│  │  └─ Atributos: cap (OpenCV capture)
│  │
│  └─ Responsabilidades:
│     • Conexión persistente con webcam
│     • Warmup de frames para estabilidad
│     • Redimensionamiento a 384×384
│     • Codificación JPEG (calidad 75)
│     • Conversión a Base64
│
├─ 📄 config.py ............................. [CONFIGURACIÓN]
│  │  └─ Constantes centralizadas:
│  │     • LM Studio (URL, modelo, API key)
│  │     • Arduino (baudrate, timeout)
│  │     • Cámara (resolución, warmup, JPEG quality)
│  │     • Aplicación (delays, debug)
│  │
│  └─ Responsabilidades:
│     • Single source of truth para todas las constantes
│     • Facilita cambios sin tocar código de módulos
│
├─ 📄 requirements.txt ....................... [DEPENDENCIAS]
│  └─ Librerías necesarias:
│     • opencv-python>=4.8.0
│     • pyserial>=3.5
│     • requests>=2.31.0
│
├─ 📄 firmware.ino .......................... [CÓDIGO ARDUINO]
│  └─ Protocolo Serial (9600 baud):
│     • '1\n'    → LED blanco (persona)
│     • '0\n'    → LED amarillo (sin persona)
│     • 'PING\n' → Responde 'PONG'
│
├─ 📄 test_connection.py ................... [PRUEBAS]
│  │  ├─ Función: test_lmstudio()
│  │  ├─ Función: test_arduino()
│  │  ├─ Función: test_camera()
│  │  ├─ Función: test_tools()
│  │  └─ Función: main()
│  │
│  └─ Uso:
│     $ python test_connection.py [--port COM3] [--camera 0]
│
├─ 📄 README.md ............................ [DOCUMENTACIÓN]
│  └─ Guía completa de instalación y uso
│
└─ 📄 .gitignore ........................... [GIT CONFIG]
   └─ Archivos a ignorar en versionado


═══════════════════════════════════════════════════════════════════════
FLUJO DE DATOS EN EL SISTEMA
═══════════════════════════════════════════════════════════════════════

                         ┌─────────────────┐
                         │   service.py    │
                         │   (ENTRADA)     │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼──────────────┐
                    │             │              │
               ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
               │camera.py│  │arduino. │  │ llm.py  │
               │         │  │  py     │  │         │
               └────┬────┘  └────┬────┘  └────┬────┘
                    │            │            │
            ┌───────▼────────────▼────────────▼───────┐
            │    LOOP PRINCIPAL (detection_loop)      │
            └───────┬────────────────────────┬────────┘
                    │                        │
              ┌─────▼─────┐         ┌────────▼────────┐
              │1. CAPTURA │         │2. ENVIAR A LLM  │
              │   IMAGEN  │         │   via requests  │
              └─────┬─────┘         └────────┬────────┘
                    │                        │
              BASE64 JPEG              Tool-calling loop
                    │                    ↓
                    │           ┌─────────────────┐
                    │           │   tools.py      │
                    │           │ execute_tool()  │
                    │           └────────┬────────┘
                    │                    │
                    └────────┬───────────┘
                             │
                        ┌────▼──────────────┐
                        │3. ACTUALIZAR      │
                        │   LEDs (Arduino)  │
                        └─────────────────┘
                             ↓
                        Resultado visual
                             ↓
                        [REPETIR CICLO]


═══════════════════════════════════════════════════════════════════════
SEGURIDAD Y CARACTERÍSTICAS AVANZADAS
═══════════════════════════════════════════════════════════════════════

✅ THREAD-SAFETY
   • arduino.py: threading.Lock() en send_command()
   • camera.py: threading.Lock() en capture_frame()
   • Permite acceso seguro desde múltiples threads

✅ AUTO-RECONEXIÓN
   • arduino.py: _ensure_connected() verifica estado
   • Si puerto se cierra, siguiente comando lo reabre
   • Tolerancia a fallos mejorada

✅ AUTO-DETECCIÓN
   • arduino.py: _find_port() busca puertos disponibles
   • Soporta Linux (/dev/ttyUSB*), Windows (COM*), macOS
   • Configurable vía --port

✅ WARMUP DE CÁMARA
   • camera.py: descarta primeros 5 frames
   • Evita capturas oscuras o inestables
   • Mejora calidad de imágenes para IA

✅ OPTIMIZACIÓN DE IMÁGENES
   • camera.py: redimensiona a 384×384 máximo
   • JPEG con calidad 75 (balance calidad/tamaño)
   • Reduce tokens en LLM, acelera inferencia

✅ MANEJO DE ERRORES
   • service.py: signal_handler() para Ctrl+C
   • Cleanup() libera recursos limpiamente
   • Try-except en loops críticos


═══════════════════════════════════════════════════════════════════════
PERSONALIZACIÓN Y EXTENSIÓN
═══════════════════════════════════════════════════════════════════════

📝 AGREGAR NUEVA HERRAMIENTA:
   1. Define función en tools.py
   2. Agrega schema JSON a TOOLS_SCHEMA
   3. Agrega entrada en AVAILABLE_FUNCTIONS
   4. Edita SYSTEM_PROMPT en llm.py para que sepa usarla

🔧 CAMBIAR MODELO LLM:
   1. config.py: LM_STUDIO_MODEL = "otro/modelo"
   2. Asegúrate de que el modelo tenga soporte de visión
   3. Ajusta LM_TEMPERATURE si es necesario

📊 AGREGAR LOGGING:
   1. Importa logging en service.py
   2. Reemplaza print() con logger.info()
   3. Exporta logs a archivo

🔌 MÚLTIPLES ARDUINOS:
   1. Crea segunda instancia de ArduinoManager
   2. Pasa a tools.py diferentes gestores
   3. Dispatch en tools según el destino

═══════════════════════════════════════════════════════════════════════
"""
