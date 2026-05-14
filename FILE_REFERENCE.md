# 📋 Referencia Rápida de Archivos

## Archivo por Archivo

### 🎯 `service.py` — Punto de Entrada
**Ejecutar:** `python service.py [--port COM3] [--camera 0]`

| Función | Responsabilidad |
|---------|---|
| `main()` | Parsea argumentos, inicializa módulos |
| `detection_loop()` | Loop infinito: captura → IA → resultado |
| `signal_handler()` | Maneja Ctrl+C para cerrar limpiamente |
| `cleanup()` | Libera cámara y puerto serial |
| `print_result_box()` | Imprime resultado decorativo |

---

### 🧠 `llm.py` — Agente de IA (HTTP/Tool-Calling)
**Modo:** Peticiones POST a LMStudio + loop agéntico

| Función | Responsabilidad |
|---------|---|
| `test_connection()` | Verifica LMStudio responde |
| `act_on_image(image_b64)` | Loop agéntico: envía imagen, ejecuta tools |
| `_make_api_call(messages)` | Petición HTTP POST a LMStudio |

**Configuración:**
- `API_URL` = `http://127.0.0.1:1234/v1/chat/completions`
- `MODEL` = `qwen/qwen3-vl-4b`
- `API_KEY` = `lm-studio`

---

### 🔧 `tools.py` — Herramientas del Agente
**Concepto:** Cada tool = (Función Python) + (Schema JSON OpenAI)

| Tool | Acción |
|------|--------|
| `person_detected()` | Enciende LED blanco → envía `'1'` a Arduino |
| `no_person()` | Enciende LED amarillo → envía `'0'` a Arduino |
| `cancel_analysis()` | Cancela sin actuar en hardware |

**Para agregar una herramienta:**
1. Define función: `def mi_tool(): ...`
2. Agrega a `TOOLS_SCHEMA` con descripción JSON
3. Agrega a `AVAILABLE_FUNCTIONS`

---

### 🔌 `arduino.py` — Comunicación Serial (Persistente + Thread-Safe)
**Clase:** `ArduinoManager`

| Método | Envía | Recibe |
|--------|-------|--------|
| `send_command(cmd)` | Comando serial | Respuesta |
| `set_led_person_detected()` | `1\n` | `OK` |
| `set_led_no_person()` | `0\n` | `OK` |
| `ping()` | `PING\n` | `PONG` |
| `close()` | — | Cierra puerto |

**Características:**
- ✅ Conexión persistente (abre 1 vez)
- ✅ Thread-safe con `threading.Lock()`
- ✅ Auto-detección de puerto (Linux/Windows/macOS)
- ✅ Auto-reconexión si puerto se cierra

---

### 📷 `camera.py` — Captura de Imágenes (Persistente + Base64)
**Clase:** `CameraManager`

| Método | Retorna |
|--------|---------|
| `capture_frame()` | Frame de OpenCV |
| `frame_to_base64(frame)` | String Base64 JPEG |
| `get_camera_data()` | Base64 listo para LLM |
| `close()` | Libera cámara |

**Optimizaciones:**
- Warmup: descarta 5 primeros frames
- Redimensiona a 384×384 máximo
- JPEG comprimido (calidad 75)
- Base64 para envío HTTP

---

### ⚙️ `config.py` — Configuración Centralizada
**Propósito:** Single source of truth para constantes

**Secciones:**
- LMStudio (host, puerto, modelo, API key)
- Arduino (baudrate, timeout, comandos)
- Cámara (resolución, warmup, JPEG quality)
- Aplicación (delays, debug)

**Uso:** Importa y usa: `from config import LM_STUDIO_MODEL`

---

### 🔧 `firmware.ino` — Código Arduino
**Protocolo Serial (9600 baud):**

```
Recibe: '1'    → enciende LED_PERSON (pin 13)
Recibe: '0'    → enciende LED_NO_PERSON (pin 8)
Recibe: 'PING' → responde 'PONG'
LEDs se apagan automáticamente después de 5 segundos
```

**Para cargar:**
1. Instala `Adafruit_VL53L0X` (si usas sensor) o solo `firmware.ino`
2. Abre en Arduino IDE
3. Selecciona puerto y placa
4. Sube el código

---

### 🧪 `test_connection.py` — Verificación del Sistema
**Uso:** `python test_connection.py [--port COM3] [--camera 0]`

| Test | Verifica |
|------|----------|
| TEST 1 | ¿LMStudio responde? |
| TEST 2 | ¿Arduino está conectado? |
| TEST 3 | ¿Cámara captura? |
| TEST 4 | ¿Herramientas disponibles? |

Flags opcionales:
- `--skip-arduino` — Omite prueba de Arduino
- `--skip-camera` — Omite prueba de cámara

---

### 📖 `README.md` — Documentación Completa
- Instalación
- Arquitectura
- Flujo de funcionamiento
- Tool-calling explicado
- Troubleshooting
- Personalización

---

### ⚡ `QUICKSTART.md` — Inicio en 5 Minutos
- Instalación rápida
- Ejecución inmediata
- Errores comunes

---

### 📋 `ARCHITECTURE.md` — Diagrama Detallado
- Estructura de directorios
- Flujo de datos
- Thread-safety
- Características avanzadas
- Extensión del sistema

---

### 📄 `requirements.txt` — Dependencias Python
```
opencv-python>=4.8.0    # Captura de cámara
pyserial>=3.5           # Serial Arduino
requests>=2.31.0        # HTTP a LMStudio
```

**Instalar:** `pip install -r requirements.txt`

---

### 📝 `.gitignore` — Git Configuration
Ignora:
- `__pycache__/` (compilados Python)
- `*.pyc` (bytecode)
- `venv/` (entorno virtual)
- `.vscode/`, `.idea/` (IDEs)
- `*.log` (logs)
- `.env` (secretos)

---

## 🔄 Flujo de Datos

```
service.py (ENTRADA)
    ↓
    ├─ camera.py  → Captura Base64
    ├─ llm.py     → Envía a LMStudio
    ├─ tools.py   → Ejecuta tool
    └─ arduino.py → Controla LEDs
    ↓
Resultado: SUCCESS/CANCEL
    ↓
[REPETIR CICLO]
```

---

## 💾 Cómo Ejecutar

### Instalación
```bash
pip install -r requirements.txt
```

### Verificar Conexiones
```bash
python test_connection.py
```

### Ejecutar Sistema
```bash
python service.py
```

### Con Opciones
```bash
python service.py --port COM3 --camera 0
```

---

## 🎓 Para Aprender

1. **Comienza aquí:** `QUICKSTART.md`
2. **Luego lee:** `README.md`
3. **Entiende arquitectura:** `ARCHITECTURE.md`
4. **Explora código:** Lee los comentarios en cada `.py`
5. **Personaliza:** Edita `config.py` y `SYSTEM_PROMPT`

---

## 🚀 Extensión del Sistema

### Agregar Nueva Herramienta
1. Define función en `tools.py`
2. Agrega schema a `TOOLS_SCHEMA`
3. Edita `SYSTEM_PROMPT` en `llm.py`

### Cambiar Modelo
1. Edita `config.py`: `LM_STUDIO_MODEL`
2. Asegúrate de que tenga soporte de visión

### Múltiples Dispositivos
1. Crea múltiples `ArduinoManager`
2. Pasa a `tools.py` según necesidad

---

**Última actualización:** 2026-05-12
**Versión:** 1.0.0
