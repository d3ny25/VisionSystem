# VisionSystem V3 — Sistema de Detección de Personas con IA Local

Arquitectura modular para detección de personas en tiempo real usando visión artificial, inteligencia artificial local (LMStudio) y Arduino.

## 🎯 Características

- **Agente Autónomo**: El LLM analiza la imagen y decide mediante tool-calling
- **100% Local**: Sin dependencias de la nube
- **HTTP Estándar**: Usa `requests` con API compatible con OpenAI
- **Thread-Safe**: Conexiones persistentes y bloqueadas con locks
- **Auto-reconectable**: Reconexión automática de puerto serial si se cierra
- **Modular**: Cada componente en su propio archivo

## 📋 Requisitos

### Software

- **Python 3.8+**
- **LMStudio** ejecutándose localmente en `http://127.0.0.1:1234`
- **Modelo VLM**: `qwen/qwen3-vl-4b` cargado en LMStudio

### Hardware

- Arduino UNO (o compatible)
- Webcam USB
- 2× LEDs (blanco y amarillo)
- Resistencias limitadoras de corriente
- Cables y protoboard

## 🏗️ Arquitectura del Sistema

### Módulos Python

| Archivo | Responsabilidad |
|---------|-----------------|
| `service.py` | **Orquestador principal** — Loop que coordina todos los módulos |
| `llm.py` | **Agente de IA** — Comunicación HTTP con LMStudio, loop agéntico |
| `tools.py` | **Herramientas** — Implementaciones Python + schemas JSON |
| `arduino.py` | **Comunicación Serial** — Conexión persistente y thread-safe con Arduino |
| `camera.py` | **Captura de imágenes** — Gestor de webcam con warmup y Base64 |
| `config.py` | **Configuración centralizada** — Todas las constantes del sistema |

### Flujo Completo

```
1. service.py inicia
   ↓
2. Verifica conexión con LMStudio
   ↓
3. Inicializa Arduino, Cámara, Módulo IA
   ↓
4. Loop infinito:
   a) Captura frame con camera.py
   b) Envía Base64 a LMStudio via llm.py
   c) LMStudio responde con tool a ejecutar
   d) Python ejecuta tool de tools.py
   e) Tool controla Arduino via arduino.py
   f) Muestra resultado y repite
```

## 🚀 Instalación Rápida

### 1. Dependencias Python

```bash
pip install -r requirements.txt
```

### 2. LMStudio

1. Descarga [LMStudio](https://lmstudio.ai/)
2. Carga el modelo:
   ```bash
   lms get qwen/qwen3-vl-4b
   ```
3. Inicia el servidor: `Developer → Local Server → Start Server` (puerto 1234)

### 3. Arduino

1. Instala `Adafruit_VL53L0X` en Arduino IDE (si usas sensor láser)
2. Carga el firmware en tu placa
3. Verifica en el Monitor Serial que responda `READY`

## ⚙️ Configuración

Edita `config.py` para cambiar:

- Puerto LMStudio y API Key
- Velocidad baudrate de Arduino (9600 recomendado)
- Resolución de cámara
- Calidad JPEG

## ▶️ Ejecución

### Opción 1: Auto-detectar todo

```bash
python service.py
```

### Opción 2: Especificar puerto y cámara

```bash
python service.py --port COM3 --camera 0
```

### Argumentos disponibles

| Argumento | Default | Descripción |
|-----------|---------|-------------|
| `--port` | Auto-detect | Puerto serial (COM3, /dev/ttyUSB0) |
| `--camera` | 0 | Índice de cámara USB |

## 📊 Ejemplo de Salida

```
══════════════════════════════════════════════════════════════════════
  🎥 SISTEMA DE VISIÓN CON DETECCIÓN DE PERSONAS
     Arquitectura Modular v1.0
══════════════════════════════════════════════════════════════════════
  Puerto Arduino  : /dev/ttyUSB0
  Índice Cámara   : 0
  Comunicación    : HTTP (requests)
  Modelo IA       : qwen/qwen3-vl-4b
══════════════════════════════════════════════════════════════════════

🟢 Conexión con LMStudio verificada
🔌 Arduino conectado en /dev/ttyUSB0 (9600 baud)
📷 Cámara inicializada (índice: 0)

[14:32:01] 📷 Ciclo 1: Capturando imagen...
[14:32:02] ✅ Imagen capturada (12345 bytes)
[14:32:02] 🧠 Ciclo 1: Analizando con IA...
[14:32:03]   🔧 IA llamando a: person_detected({})
[14:32:03] 💭 Ejecutando: person_detected

    🟢 👤 PERSON

[14:32:03] 📊 Resultado final: SUCCESS:PERSON:DETECTED
```

## 🔧 Cómo Funciona `requests`

`llm.py` usa `requests` para hacer peticiones HTTP POST a LMStudio:

```python
response = requests.post(
    "http://127.0.0.1:1234/v1/chat/completions",
    headers={"Authorization": "Bearer lm-studio"},
    json={
        "model": "qwen/qwen3-vl-4b",
        "messages": [...],
        "tools": TOOLS_SCHEMA,
        "tool_choice": "auto"
    }
)
```

**Ventajas:**
- Compatible con cualquier servidor OpenAI-compatible
- API Key explícita en cada petición
- Código transparente — se ve exactamente qué se envía/recibe

## 🤖 Loop Agéntico (Tool-Calling)

```
┌─────────────────────────────────────────────────────────┐
│              LOOP AGÉNTICO (máx. 5 iteraciones)         │
│                                                         │
│ 1. Python envía imagen en Base64 + tools schema        │
│ 2. LLM analiza y decide qué tool llamar               │
│ 3. LLM responde con tool_calls (nombre + argumentos)  │
│ 4. Python ejecuta la función localmente               │
│ 5. Python devuelve resultado al LLM                   │
│ 6. Si SUCCESS/CANCEL → termina                        │
│ 7. Si no → LLM puede pedir otra tool → vuelve a 2     │
└─────────────────────────────────────────────────────────┘
```

## 📝 Protocolo Serial Arduino

| Comando | Respuesta | Acción |
|---------|-----------|--------|
| `1\n` | `OK` | Enciende LED blanco (persona detectada) |
| `0\n` | `OK` | Enciende LED amarillo (sin persona) |
| `PING\n` | `PONG` | Verificación de conexión |

## 🐛 Solución de Problemas

| Problema | Solución |
|----------|----------|
| "Error conectando Arduino" | Verifica puerto COM/USB y permisos. En Linux: `sudo usermod -a -G dialout $USER` |
| "Cámara no abre" | Cambia índice con `--camera 1`, `--camera 2`, etc. |
| "LMStudio no responde" | Verifica http://127.0.0.1:1234 en navegador. Asegúrate de que el servidor esté en `Developer → Local Server` |
| "LLM no decide" | Ajusta el system prompt en `llm.py` para ser más claro |

## 📦 Dependencias

```
opencv-python>=4.8.0     # Captura de cámara
pyserial>=3.5            # Comunicación Arduino
requests>=2.31.0         # Peticiones HTTP
```

## 🎓 Estructura del Proyecto

```
VisionSystem V3/
├── service.py           # ▶ PUNTO DE ENTRADA
├── llm.py               # Agente de IA
├── tools.py             # Herramientas del agente
├── arduino.py           # Comunicación serial
├── camera.py            # Captura de imágenes
├── config.py            # Configuración centralizada
├── requirements.txt     # Dependencias
└── README.md           # Este archivo
```

## 💡 Personalizaciones Comunes

### Agregar nueva lógica de detección

Edita el `SYSTEM_PROMPT` en `llm.py`:

```python
SYSTEM_PROMPT = """Your task: Detect specific objects...
RULES:
- If you see a cat → call person_detected()  # Rename the tool!
- If no cat → call no_person()
"""
```

### Cambiar puerto LMStudio

En `config.py`:

```python
LM_STUDIO_PORT = 1235  # Cambiar a tu puerto
```

### Agregar más herramientas

1. Define función en `tools.py`
2. Agrega schema JSON a `TOOLS_SCHEMA`
3. Agrega entrada en `AVAILABLE_FUNCTIONS`

## 📚 Referencias

- [OpenCV Documentation](https://docs.opencv.org/)
- [Arduino Documentation](https://www.arduino.cc/reference/)
- [LMStudio](https://lmstudio.ai/)
- [Requests Library](https://requests.readthedocs.io/)
- [PySerial](https://pyserial.readthedocs.io/)

## 👥 Autor

Basado en la arquitectura modular del Clasificador-de-frutas V4

## 📄 Licencia

MIT

---

**Nota:** Este es un proyecto académico y experimental. Utilízalo para aprendizaje, investigación y prototipado.
