"""
llm.py — Agente de IA (Loop Agéntico)

Contiene toda la lógica de comunicación con LMStudio y el loop de tool-calling. 
No tiene estado: recibe imagen en Base64, ejecuta el loop y devuelve el resultado final.

Usa la librería `requests` para hacer peticiones HTTP a LMStudio (compatible con API OpenAI).
"""

import requests
import json
import base64
import re
from typing import Optional, Callable
import tools


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

API_URL = "http://127.0.0.1:1234/v1/chat/completions"
LMSTUDIO_MODEL = "qwen/qwen3-vl-4b"
LMSTUDIO_API_KEY = "sk-lm-aRiEz0zg:CwVZ1egWOiLzZh50VBWe"

# System prompt que define el comportamiento del agente
SYSTEM_PROMPT = """You are an autonomous person detection system for a vision application.

Your task: Analyze the provided image and determine if there are people present.

RULES:
- If you see at least ONE person (any body part, face, or clear human silhouette) → call person_detected()
- If the image shows an empty space or no humans at all → call no_person()
- If the image is too blurry or unrecognizable → call cancel_analysis()

IMPORTANT:
- Be decisive: one analysis, one tool call, then stop
- No explanations, just identify and call the appropriate tool
- Trust your visual analysis — if unsure, default to the most likely scenario
"""

MAX_ITERATIONS = 5  # Máximo número de iteraciones del loop agéntico


# ============================================================================
# FUNCIONES DE SOPORTE
# ============================================================================

def test_connection() -> bool:
    """Verifica que LMStudio responde antes de iniciar el loop."""
    try:
        response = requests.get(
            f"{API_URL.rsplit('/v1', 1)[0]}/v1/models",
            headers={"Authorization": f"Bearer {LMSTUDIO_API_KEY}"},
            timeout=5
        )
        if response.status_code == 200:
            print("🟢 Conexión con LMStudio verificada")
            return True
        else:
            print(f"❌ LMStudio no responde correctamente: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando con LMStudio: {e}")
        return False


def _make_api_call(messages: list) -> Optional[dict]:
    """
    Realiza una petición HTTP a LMStudio.
    
    Args:
        messages: Historial de mensajes para la conversación
    
    Returns:
        Respuesta JSON de LMStudio o None si falla
    """
    try:
        payload = {
            "model": LMSTUDIO_MODEL,
            "messages": messages,
            "tools": tools.TOOLS_SCHEMA,
            "tool_choice": "auto",
            "temperature": 0.3,  # Más determinístico para detección
            "max_tokens": 256
        }
        
        response = requests.post(
            API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LMSTUDIO_API_KEY}"
            },
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error en API: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        print(f"❌ Excepción en API: {e}")
        return None


# ============================================================================
# LOOP AGÉNTICO PRINCIPAL
# ============================================================================

def act_on_image(image_b64: str, on_message: Optional[Callable] = None) -> str:
    """
    Ejecuta el loop agéntico completo para analizar una imagen.
    
    Args:
        image_b64: Imagen codificada en Base64
        on_message: Callback opcional para mensajes en tiempo real
    
    Returns:
        Resultado final: "SUCCESS:..." o "ERROR:..." o "CANCEL:..."
    """
    
    if not image_b64:
        return "ERROR:Imagen vacía"
    
    # Inicializar historial de mensajes
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_b64}"
                    }
                },
                {
                    "type": "text",
                    "text": "Analyze this image. Are there any people? Call the appropriate tool."
                }
            ]
        }
    ]
    
    if on_message:
        on_message("assistant", "Iniciando análisis...")
    
    # Loop agéntico
    iteration = 0
    while iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n🔄 Iteración {iteration}/{MAX_ITERATIONS}")
        
        # Llamar al LLM
        response = _make_api_call(messages)
        if response is None:
            return "ERROR:LMStudio no responde"
        
        # Parsear respuesta
        try:
            assistant_msg = response.get("choices", [{}])[0].get("message", {})
            finish_reason = response.get("choices", [{}])[0].get("finish_reason")
            
            # Agregar respuesta del asistente al historial
            messages.append({"role": "assistant", "content": assistant_msg.get("content", "")})
            
            # Verificar si hay tool calls
            tool_calls = assistant_msg.get("tool_calls", [])
            
            if tool_calls:
                # Procesar tool calls
                for tool_call in tool_calls:
                    tool_name = tool_call.get("function", {}).get("name")
                    tool_args_str = tool_call.get("function", {}).get("arguments", "{}")
                    
                    # Parsear argumentos JSON
                    try:
                        tool_args = json.loads(tool_args_str)
                    except json.JSONDecodeError:
                        tool_args = {}
                    
                    print(f"  🔧 IA llamando a: {tool_name}({tool_args})")
                    
                    if on_message:
                        on_message("tool", f"Ejecutando: {tool_name}")
                    
                    # Ejecutar herramienta
                    result = tools.execute_tool(tool_name, tool_args)
                    print(f"  ✅ Resultado: {result}")
                    
                    # Agregar resultado al historial
                    messages.append({
                        "role": "tool",
                        "tool_use_id": tool_call.get("id", ""),
                        "content": result
                    })
                    
                    # Verificar si debemos terminar
                    if result.startswith("SUCCESS") or result.startswith("CANCEL"):
                        return result
                    
            elif finish_reason == "stop":
                # El LLM terminó sin llamar tool (caso inesperado)
                return "ERROR:LLM finalizó sin decisión"
            else:
                # Seguir iterando
                pass
        
        except Exception as e:
            print(f"❌ Error procesando respuesta: {e}")
            return f"ERROR:Excepción: {str(e)}"
    
    return "ERROR:Máximo número de iteraciones alcanzado"
