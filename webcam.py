from fastmcp import FastMCP
import cv2
import base64
import requests
import time
from fastmcp.utilities.types import Image
import serial
import json
import re

app = FastMCP(name="Vision System")

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "qwen3-vl-4b"

requests_session = requests.Session()
last_image_base64 = None
camera_index = None

try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    print("Arduino conectado")
except:
    arduino = None
    print("Arduino no conectado")


def find_external_camera(max_cameras=5):
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                available_cameras.append((i, w * h))
                print(f"Camera {i} detectada - {w}x{h}")
            cap.release()
    if not available_cameras:
        return None
    available_cameras.sort(key=lambda x: x[1], reverse=True)
    return available_cameras[0][0]


def capture_image():
    global last_image_base64, camera_index
    if camera_index is None:
        camera_index = find_external_camera()
    if camera_index is None:
        return None, None

    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return None, None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None, None

    _, buffer = cv2.imencode(".jpg", frame)
    last_image_base64 = base64.b64encode(buffer).decode("utf-8")

    image_obj = Image(data=buffer, format="jpeg")
    return image_obj.to_image_content(), last_image_base64


def check_lmstudio():
    try:
        r = requests_session.get("http://127.0.0.1:1234/v1/models", timeout=3)
        return r.status_code == 200
    except:
        return False


def analyze_image(image_base64: str) -> dict:
    if not check_lmstudio():
        return {"error": "LM Studio no está corriendo"}

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Analiza esta imagen y responde SOLO con JSON válido, sin texto adicional:
{
  "people_detected": true/false,
  "people_count": número,
  "objects": ["lista", "de", "objetos"],
  "description": "descripción breve en español"
}"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    for attempt in range(3):
        try:
            response = requests_session.post(LM_STUDIO_URL, json=payload, timeout=20)
            if response.status_code != 200:
                continue

            content = response.json()["choices"][0]["message"]["content"]
            print("🧾 Respuesta modelo:", content)

            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                data = json.loads(match.group(0))

                # Enviar señal al Arduino
                if arduino:
                    signal = b'1' if data.get("people_detected") else b'0'
                    arduino.write(signal)
                    print(f"📡 Arduino: {'LED ON' if signal == b'1' else 'LED OFF'}")

                return data

        except requests.exceptions.Timeout:
            print(f"⏱ Timeout intento {attempt + 1}")
        except Exception as e:
            return {"error": str(e)}
        time.sleep(1)

    return {"error": "Falló después de 3 intentos"}


# TOOL PRINCIPAL — retorna imagen + análisis juntos
@app.tool
def capture_webcam() -> list:
    """Toma una foto con la webcam, la muestra y analiza su contenido."""
    print("Capturando imagen...")

    image_content, image_base64 = capture_image()

    if image_content is None:
        return [{"type": "text", "text": "No se pudo acceder a la cámara."}]

    print("Analizando imagen...")
    analysis = analyze_image(image_base64)

    # Formatear resultado del análisis
    if "error" in analysis:
        analysis_text = f"Error al analizar: {analysis['error']}"
    else:
        people = analysis.get("people_count", 0)
        objects = ", ".join(analysis.get("objects", [])) or "ninguno"
        description = analysis.get("description", "Sin descripción")
        analysis_text = (
            f"**Análisis de la imagen:**\n"
            f"- Personas detectadas: {people}\n"
            f"- Objetos: {objects}\n"
            f"- Descripción: {description}"
        )

    # Retornar imagen Y texto juntos
    return [
        image_content,
        {"type": "text", "text": analysis_text}
    ]


@app.tool
def robot_status():
    return {"connection": "ready"}


if __name__ == "__main__":
    app.run()