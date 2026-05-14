# ⚡ QUICKSTART - Inicio Rápido

## 🎯 En 5 minutos

### Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 2: Verificar Conexiones

```bash
python test_connection.py
```

Este comando verifica:
- ✅ LMStudio responde
- ✅ Arduino está conectado
- ✅ Cámara funciona
- ✅ Herramientas disponibles

### Paso 3: Ejecutar el Sistema

```bash
python service.py
```

O con opciones específicas:

```bash
python service.py --port COM3 --camera 0
```

---

## 🔧 Requisitos Previos

### LMStudio
1. Descarga [LMStudio](https://lmstudio.ai/)
2. Instala el modelo:
   ```bash
   lms get qwen/qwen3-vl-4b
   ```
3. Inicia el servidor: `Developer → Local Server → Start Server`
4. Verifica que está en `http://127.0.0.1:1234`

### Arduino
1. Conecta Arduino al puerto USB
2. Carga el firmware `firmware.ino` usando Arduino IDE
3. Verifica el puerto en `Device Manager` (Windows) o `ls /dev/ttyUSB*` (Linux)

### Cámara
- Cualquier webcam USB compatible con OpenCV

---

## 📊 Ejemplo de Salida

```
══════════════════════════════════════════════════════════════════════
  🎥 SISTEMA DE VISIÓN CON DETECCIÓN DE PERSONAS
══════════════════════════════════════════════════════════════════════
  Puerto Arduino  : /dev/ttyUSB0
  Índice Cámara   : 0
  Comunicación    : HTTP (requests)
  Modelo IA       : qwen/qwen3-vl-4b
══════════════════════════════════════════════════════════════════════

🟢 Sistema iniciado. Presiona Ctrl+C para salir.

[14:32:01] 📷 Ciclo 1: Capturando imagen...
[14:32:02] ✅ Imagen capturada (12345 bytes)
[14:32:02] 🧠 Ciclo 1: Analizando con IA...
[14:32:03]   🔧 IA llamando a: person_detected({})

    🟢 👤 PERSON

[14:32:03] 📊 Resultado final: SUCCESS:PERSON:DETECTED
```

---

## 🐛 Problemas Comunes

| Error | Solución |
|-------|----------|
| `Connection refused` | LMStudio no está corriendo. Inicia: `Developer → Local Server` |
| `No port found` | Arduino no está conectado o uso incorrecto. Especifica: `--port COM3` |
| `Camera not found` | Intenta otro índice: `--camera 1`, `--camera 2` |
| `Permission denied (Linux)` | Agrega permisos: `sudo usermod -a -G dialout $USER` |

---

## 📁 Archivos Importantes

- **service.py** ← Ejecuta esto
- **llm.py** ← Comunicación con IA
- **tools.py** ← Herramientas (LEDs)
- **arduino.py** ← Comunicación con Arduino
- **camera.py** ← Captura de imagen
- **config.py** ← Configuración

---

## 🚀 Siguientes Pasos

1. Lee [README.md](README.md) para documentación completa
2. Revisa [ARCHITECTURE.md](ARCHITECTURE.md) para entender la estructura
3. Modifica `SYSTEM_PROMPT` en `llm.py` para personalizar el comportamiento
4. Agrega nuevas herramientas en `tools.py`

---

**¿Preguntas?** Revisa los comentarios en el código o lee la documentación completa.
