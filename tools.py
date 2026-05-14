"""
tools.py — Herramientas del Agente

Define las funciones que el LLM puede invocar. Cada tool tiene dos partes:

1. Implementación Python — La función real que ejecuta la acción
2. Schema JSON (OpenAI format) — La descripción que se envía al LLM 
   para que sepa cuándo y cómo llamar cada herramienta

Los tools disponibles:
- person_detected() — Activa LED blanco
- no_person() — Activa LED amarillo
- cancel() — Descarta sin acción
"""

import json
from typing import Callable, Dict, Any, Optional


# Será asignado por service.py antes de usar los tools
arduino_manager = None


def set_arduino_manager(manager):
    """Inyecta la instancia de ArduinoManager."""
    global arduino_manager
    arduino_manager = manager


# ============================================================================
# IMPLEMENTACIONES PYTHON DE LAS HERRAMIENTAS
# ============================================================================

def person_detected() -> str:
    """
    Activa el LED blanco indicando que se detectó una persona.
    
    Returns:
        Mensaje de confirmación
    """
    global arduino_manager
    
    if arduino_manager is None or arduino_manager.ser is None:
        # Arduino no conectado - devolver éxito sin acción física
        return "SUCCESS:PERSON:DETECTED:NO_HARDWARE"
    
    try:
        success = arduino_manager.set_led_person_detected()
        if success:
            return "SUCCESS:PERSON:DETECTED"
        else:
            return "ERROR:Fallo al controlar Arduino"
    except Exception as e:
        return f"ERROR:{str(e)}"


def no_person() -> str:
    """
    Activa el LED amarillo indicando que NO se detectó persona.
    
    Returns:
        Mensaje de confirmación
    """
    global arduino_manager
    
    if arduino_manager is None or arduino_manager.ser is None:
        # Arduino no conectado - devolver éxito sin acción física
        return "SUCCESS:NO_PERSON:DETECTED:NO_HARDWARE"
    
    try:
        success = arduino_manager.set_led_no_person()
        if success:
            return "SUCCESS:NO_PERSON:DETECTED"
        else:
            return "ERROR:Fallo al controlar Arduino"
    except Exception as e:
        return f"ERROR:{str(e)}"


def cancel_analysis() -> str:
    """
    Cancela el análisis sin realizar acción de hardware.
    
    Returns:
        Mensaje de cancelación
    """
    return "CANCEL:Análisis cancelado"


# ============================================================================
# SCHEMAS JSON (FORMATO OPENAI)
# ============================================================================

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "person_detected",
            "description": "Activa el LED blanco de la máquina cuando se detecta al menos una persona en la imagen. Use esta herramienta cuando identifique presencia humana clara.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "no_person",
            "description": "Activa el LED amarillo cuando NO se detecta ninguna persona en la escena. Use esta herramienta cuando la imagen muestre un espacio vacío o sin humanos.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_analysis",
            "description": "Cancela el análisis si la imagen es muy borrosa, irreconocible o no contiene información clara. No activa LEDs.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# ============================================================================
# MAPA DE FUNCIONES (DISPATCH DINÁMICO)
# ============================================================================

AVAILABLE_FUNCTIONS: Dict[str, Callable] = {
    "person_detected": person_detected,
    "no_person": no_person,
    "cancel_analysis": cancel_analysis,
}


def execute_tool(tool_name: str, tool_args: Dict[str, Any]) -> str:
    """
    Ejecuta una herramienta por nombre dinámicamente.
    
    Args:
        tool_name: Nombre de la herramienta (ej: "person_detected")
        tool_args: Argumentos para la herramienta (usualmente vacío)
    
    Returns:
        Resultado de la ejecución
    """
    if tool_name not in AVAILABLE_FUNCTIONS:
        return f"ERROR:Herramienta no reconocida: {tool_name}"
    
    try:
        func = AVAILABLE_FUNCTIONS[tool_name]
        result = func(**tool_args) if tool_args else func()
        return result
    except Exception as e:
        return f"ERROR:Excepción al ejecutar {tool_name}: {str(e)}"
