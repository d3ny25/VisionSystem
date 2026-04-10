# Sistema de Visión Artificial con Inteligencia Artificial, MCP y Arduino

## Portada

**Materia:** Inteligencia Artificial 1

**Proyecto:** Sistema de visión artificial para detección de personas con activación de LEDs mediante Arduino

**Equipo de trabajo:**

* Alan Fernando Sánchez Romero
* Daniel Benítez
* Juan Eduardo Fuentes Cruz
* Luis Antonio Sánchez Sánchez

---

## 1. Introducción

El presente proyecto consiste en el desarrollo de un sistema de visión artificial capaz de detectar personas en tiempo real mediante el uso de inteligencia artificial local y comunicación con hardware embebido. La solución integra una cámara web como dispositivo de captura visual, un modelo multimodal ejecutado localmente en LM Studio para el análisis de imágenes, y una placa Arduino encargada de responder físicamente mediante indicadores luminosos.

La finalidad principal del sistema es demostrar la integración entre software y hardware en un entorno funcional, donde la inteligencia artificial no solo interpreta información visual, sino que también genera una reacción en el mundo físico. Esta interacción permite comprender de manera práctica conceptos fundamentales de automatización, análisis visual, comunicación serial, procesamiento de imágenes y arquitectura de servicios basados en herramientas MCP.

Además, el proyecto refleja un enfoque moderno de desarrollo, ya que utiliza inteligencia artificial local en lugar de servicios en la nube. Esto permite mantener un mayor control sobre el flujo de datos, reducir la dependencia de internet y mejorar la privacidad de las imágenes capturadas. De esta manera, el sistema no solo funciona como una demostración académica, sino también como una base técnica para futuras aplicaciones en vigilancia, control de acceso o monitoreo inteligente.

---

## 2. Descripción general del proyecto

Este sistema fue diseñado para capturar imágenes en tiempo real, analizarlas mediante un modelo de inteligencia artificial local y determinar si existe presencia humana en el entorno observado. A partir de esa evaluación, el sistema envía una señal a Arduino para activar uno de dos LEDs:

* **LED blanco:** se enciende cuando se detecta al menos una persona.
* **LED amarillo:** se enciende cuando no se detecta ninguna persona.

Además de realizar la detección, el sistema también genera una descripción breve del contenido de la imagen e identifica algunos objetos presentes en la escena. Todo esto se realiza de forma local, sin depender de servicios externos en la nube, lo que mejora el control del proceso y protege la privacidad de las imágenes capturadas.

El flujo de trabajo del sistema se puede resumir de la siguiente forma: primero se detecta la cámara disponible en el equipo; después se toma una imagen; posteriormente se envía al modelo multimodal de LM Studio; luego se interpreta la respuesta en formato JSON; finalmente, se transmite un comando por puerto serial a Arduino para encender el LED correspondiente. Este comportamiento convierte al sistema en una solución cerrada, funcional y altamente demostrativa.

---

## 3. Objetivos del proyecto

### Objetivo general

Diseñar e implementar un sistema de visión artificial capaz de detectar personas en tiempo real mediante inteligencia artificial local y activar indicadores físicos a través de Arduino.

### Objetivos específicos

* Capturar imágenes desde una cámara web de manera automática.
* Procesar las imágenes con un modelo multimodal ejecutado en LM Studio.
* Estructurar la salida del modelo en formato JSON para facilitar su interpretación.
* Comunicar el resultado del análisis a una placa Arduino mediante puerto serial.
* Controlar LEDs indicadores según el estado de detección.
* Integrar una herramienta MCP que exponga funciones reutilizables para el sistema.
* Aplicar principios de modularidad, automatización y manejo de errores.

---

## 4. Alcance del sistema

El proyecto cubre las siguientes funciones:

* Detección automática de cámaras disponibles en el equipo.
* Captura de una imagen desde la cámara seleccionada.
* Conversión de la imagen a un formato compatible con el modelo de IA.
* Envío de la imagen al modelo local de LM Studio.
* Recepción de una respuesta estructurada con información visual.
* Interpretación de la respuesta para determinar si hay personas.
* Envío de una señal binaria a Arduino.
* Activación de LEDs como respuesta visual.
* Apagado automático de los LEDs después de un tiempo definido.

El sistema está enfocado principalmente en fines académicos, demostrativos y experimentales, aunque su estructura puede servir como base para aplicaciones más avanzadas en vigilancia, control de acceso, automatización inteligente o asistencia visual.

---

## 5. Descripción del hardware

Uno de los componentes más importantes del proyecto es la parte física, ya que es la que permite materializar en el mundo real la respuesta generada por la inteligencia artificial. El hardware utilizado fue seleccionado con el objetivo de mantener una implementación sencilla, económica y funcional, sin perder capacidad de demostración.

### 5.1. Cámara web

La cámara web es el dispositivo encargado de capturar las imágenes que posteriormente son analizadas por el modelo de IA. En este proyecto se utilizó una cámara compatible con el sistema operativo y reconocida por OpenCV mediante índices de dispositivo. La aplicación realiza una búsqueda automática de cámaras disponibles, prueba cada una de ellas y selecciona la que ofrece una captura válida.

La resolución de captura fue configurada en **1280x720 píxeles**, lo que proporciona un equilibrio adecuado entre calidad visual y velocidad de procesamiento. Esta resolución permite que el modelo de inteligencia artificial reciba una imagen suficientemente clara para detectar personas y objetos sin incrementar excesivamente el tiempo de análisis.

### 5.2. Placa Arduino

La placa Arduino actúa como el módulo de salida física del sistema. Su función principal es recibir una señal binaria desde Python por medio de comunicación serial y activar el LED correspondiente. Aunque el código es compatible con diferentes placas de la familia Arduino, el funcionamiento descrito corresponde a una configuración típica de puerto serial USB con velocidad de transmisión de **9600 baudios**.

Arduino fue elegido porque ofrece una plataforma estable, fácil de programar y ampliamente utilizada en proyectos de automatización y electrónica básica. Su integración con Python mediante `pyserial` permite una comunicación directa y confiable entre el análisis de software y la respuesta del hardware.

### 5.3. LEDs indicadores

El circuito utiliza dos LEDs como indicadores visuales de estado:

* **LED blanco:** indica que el sistema detectó al menos una persona.
* **LED amarillo:** indica que no se detectó ninguna persona.

Estos LEDs fueron conectados a pines digitales específicos de Arduino, de acuerdo con el código cargado en la placa. Su uso permite que la respuesta del sistema sea clara, inmediata y fácilmente observable por cualquier usuario.

### 5.4. Resistencias y elementos de conexión

Para garantizar un funcionamiento seguro y evitar daños en los componentes, cada LED debe utilizar una resistencia limitadora de corriente. En una implementación típica, estas resistencias se colocan en serie con los LEDs para controlar el paso de corriente desde los pines digitales de Arduino. Además, se emplean cables Dupont y una protoboard para realizar las conexiones de forma ordenada y flexible.

### 5.5. Alimentación y conexión física

El sistema se alimenta principalmente desde el puerto USB del equipo de cómputo, que cumple una doble función: suministrar energía a la placa Arduino y establecer la comunicación serial con el programa desarrollado en Python. Esta configuración facilita el montaje, ya que no requiere una fuente externa adicional para la parte de control.

### 5.6 Maqueta final

[Maqueta](/images/Maqueta.jpeg)

---

## 6. Configuración del hardware

La configuración física del sistema se llevó a cabo siguiendo una estructura simple pero ordenada, con el objetivo de asegurar estabilidad en la comunicación entre la computadora, la cámara y la placa Arduino.

### 6.1. Configuración de la cámara

La cámara web se conectó directamente al equipo mediante puerto USB. Posteriormente, el programa en Python utilizó OpenCV para detectar automáticamente los dispositivos disponibles. Para ello, se evaluaron varios índices de cámara, verificando cuál de ellos devolvía una imagen válida. Una vez detectada la cámara activa, se seleccionó la de mayor resolución disponible dentro del conjunto encontrado.

Este método evita la necesidad de seleccionar manualmente el dispositivo cada vez que se ejecuta el proyecto. Además, permite trabajar en equipos donde existen varias cámaras conectadas, ya que el sistema puede identificar la mejor opción de manera automática.

### 6.2. Configuración de Arduino

La placa Arduino se configuró para trabajar como receptor de comandos seriales provenientes de Python. En el código cargado en la placa se definieron dos pines de salida:

* **Pin 13** para el LED asociado a la detección de personas.
* **Pin 8** para el LED asociado a la ausencia de personas.

Ambos pines se inicializaron como salidas digitales mediante la instrucción `pinMode()`. Posteriormente, se apagaron al inicio del programa con `digitalWrite(..., LOW)` para garantizar que el circuito arrancara en un estado seguro.

La comunicación serial se inició con la sentencia:

```cpp
Serial.begin(9600);
```

Esta velocidad coincide con la configurada en Python (`9600` baudios), lo cual asegura que ambos sistemas interpreten los datos transmitidos de forma correcta.

### 6.3. Conexión de los LEDs

Cada LED se conectó a un pin digital diferente de Arduino. El cátodo de cada LED se conectó a tierra (GND) y el ánodo se vinculó al pin de salida correspondiente a través de una resistencia limitadora de corriente. Esta disposición permite que la placa controle el encendido y apagado de los indicadores sin comprometer la integridad eléctrica de los componentes.

### 6.4. Lógica de funcionamiento del hardware

El comportamiento del hardware se basa en una lógica binaria simple:

* Si Arduino recibe el carácter `'1'`, se activa el LED de detección de persona.
* Si Arduino recibe el carácter `'0'`, se activa el LED de ausencia de persona.
* Después de un tiempo definido, ambos LEDs se apagan automáticamente.

Este diseño garantiza una respuesta visual clara y evita que los LEDs permanezcan encendidos de forma indefinida.

[Maquetado Arduino](/images/Arduino.jpeg)

---

## 7. Arquitectura general del sistema

El proyecto está dividido en tres componentes principales que trabajan de forma coordinada:

### 7.1. Capa de captura de imagen

Esta capa está implementada en Python utilizando OpenCV. Su función es detectar cámaras conectadas al equipo, seleccionar la más adecuada y capturar una imagen en tiempo real.

### 7.2. Capa de inteligencia artificial

Esta capa utiliza LM Studio como servidor local de inferencia y el modelo **qwen3-vl-4b**, capaz de analizar tanto texto como imágenes. El sistema envía una solicitud HTTP con la imagen codificada y recibe una respuesta estructurada en formato JSON.

### 7.3. Capa de actuación física

Está compuesta por Arduino y dos LEDs. Esta capa recibe la señal enviada desde Python por medio de comunicación serial y activa el LED correspondiente según el resultado del análisis.

---

## 8. Herramienta MCP y su función dentro del sistema

Uno de los elementos más importantes del proyecto es el uso de **FastMCP**, que permite exponer funcionalidades como herramientas accesibles desde un entorno compatible con MCP.

### 8.1. ¿Qué es MCP en este proyecto?

MCP, o **Model Context Protocol**, se utiliza aquí como una capa de integración que permite organizar capacidades del sistema en herramientas reutilizables. En lugar de tener un script aislado, el proyecto se estructura como un servicio que ofrece funciones concretas, como capturar una imagen o verificar el estado del sistema.

### 8.2. Implementación con FastMCP

Se creó una aplicación MCP con el nombre **Vision System**. Esta aplicación expone al menos dos herramientas:

* **capture_webcam()**: toma una fotografía, la analiza y devuelve la imagen junto con un resumen textual.
* **robot_status()**: retorna el estado general de conexión del sistema.

### 8.3. Ventajas del enfoque MCP

El uso de MCP aporta varias ventajas:

* Modularidad del código.
* Reutilización de funciones.
* Mejor organización del sistema.
* Posibilidad de integrar el proyecto con otros clientes o agentes compatibles.
* Separación clara entre captura, análisis y control físico.

---

## 9. Configuración del software

### 9.1. Lenguaje y entorno de desarrollo

El sistema fue desarrollado en **Python**, ya que permite integrar de forma sencilla visión artificial, comunicación serial, consumo de APIs y estructuración de servicios mediante MCP.

### 9.2. Bibliotecas utilizadas

Se emplearon las siguientes librerías:

* **fastmcp**: para crear el servidor MCP y exponer herramientas.
* **cv2 (OpenCV)**: para la captura y manejo de imágenes desde la cámara.
* **base64**: para codificar la imagen en un formato transmitible.
* **requests**: para enviar peticiones HTTP a LM Studio.
* **time**: para pausas y control temporal.
* **serial (pyserial)**: para la comunicación con Arduino.
* **json**: para interpretar respuestas estructuradas.
* **re**: para extraer el JSON desde la respuesta del modelo.

### 9.3. Modelo de IA utilizado

Se utilizó el modelo **qwen3-vl-4b** cargado en **LM Studio**. Este modelo fue elegido por su capacidad multimodal, es decir, porque puede analizar simultáneamente texto e imágenes.

### 9.4. Configuración de LM Studio

LM Studio fue ejecutado en modo local y expuesto como servicio en la ruta:

```python
http://127.0.0.1:1234/v1/chat/completions
```

Para verificar su disponibilidad, el sistema realiza una consulta previa al endpoint:

```python
http://127.0.0.1:1234/v1/models
```

Si el servicio responde correctamente, entonces el análisis visual puede ejecutarse. En caso contrario, el programa devuelve un mensaje de error para evitar fallos silenciosos.

### 9.5. Estructura de la petición al modelo

La imagen capturada se convierte a formato **Base64** para poder ser enviada dentro de una solicitud HTTP. El mensaje enviado al modelo solicita explícitamente una respuesta en formato JSON válido, con la siguiente estructura lógica:

```json
{
  "people_detected": true,
  "people_count": 1,
  "objects": ["mesa", "computadora"],
  "description": "Se observa una persona frente a una mesa en un entorno interior."
}
```

Este formato facilita la lectura automática de la respuesta y permite tomar decisiones en función de la presencia o ausencia de personas.

---

## 10. Explicación del código del MCP

El script de MCP fue diseñado para integrar la captura de imagen, el análisis visual y la comunicación con Arduino en una sola aplicación modular.

### 10.1. Inicialización general

El programa comienza importando las librerías necesarias y creando la instancia principal de FastMCP:

```python
app = FastMCP(name="Vision System")
```

También se definen constantes como la URL del servicio de LM Studio y el nombre del modelo multimodal:

```python
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "qwen3-vl-4b"
```

Además, se crea una sesión persistente de `requests` para optimizar el envío de peticiones HTTP.

### 10.2. Conexión con Arduino

Se intenta abrir el puerto serial `COM3` a **9600 baudios**:

```python
arduino = serial.Serial('COM3', 9600, timeout=1)
```

En caso de que la placa no esté conectada o no se encuentre el puerto, el programa continúa ejecutándose sin interrumpirse, asignando `None` a la variable `arduino`. Esta decisión mejora la tolerancia a fallos y permite probar la parte visual del sistema incluso sin hardware conectado.

### 10.3. Detección automática de cámara

La función `find_external_camera()` recorre varios índices de cámara disponibles y verifica cuáles pueden capturar imagen. Para cada cámara detectada, se evalúa la resolución de la imagen obtenida y se selecciona la de mayor tamaño. Este criterio ayuda a escoger la cámara con mejor calidad disponible.

### 10.4. Captura de imagen

La función `capture_image()` abre la cámara seleccionada, configura la resolución en **1280x720** y toma una sola captura. Luego, la imagen se codifica en formato JPEG y después en Base64 para su envío al modelo.

### 10.5. Análisis con IA

La función `analyze_image()` construye el mensaje destinado a LM Studio. En él se solicita al modelo que analice la escena y responda únicamente con JSON. Posteriormente, la respuesta se procesa con expresiones regulares para extraer el bloque JSON y convertirlo en un diccionario de Python.

Si se detecta una o más personas, el sistema envía el carácter `'1'` a Arduino. En caso contrario, envía `'0'`.

### 10.6. Herramienta principal `capture_webcam()`

Esta herramienta representa el núcleo funcional del sistema. Ejecuta los siguientes pasos:

1. Captura la imagen desde la webcam.
2. Envía la imagen al modelo de IA.
3. Recibe el análisis estructurado.
4. Construye un texto resumen.
5. Retorna tanto la imagen como la descripción del análisis.

Este diseño permite que la herramienta sea útil tanto para una interfaz humana como para otros agentes o clientes que consuman el servicio MCP.

### 10.7. Herramienta `robot_status()`

La función `robot_status()` se utiliza como un método simple de verificación. Devuelve un estado de conexión listo para confirmar que el servicio MCP está operativo.

---

## 11. Explicación del código de Arduino

El programa cargado en Arduino fue diseñado para recibir comandos simples desde la computadora y ejecutar una respuesta física inmediata.

### 11.1. Declaración de pines

Se definieron dos pines digitales:

```cpp
const int ledPin1 = 13;
const int ledPin2 = 8;
```

El pin 13 se asocia al LED que representa detección de personas, mientras que el pin 8 se asigna al LED que representa ausencia de personas.

### 11.2. Configuración inicial

En la función `setup()` se configuran ambos pines como salidas y se apagan al inicio:

```cpp
pinMode(ledPin1, OUTPUT);
pinMode(ledPin2, OUTPUT);
digitalWrite(ledPin1, LOW);
digitalWrite(ledPin2, LOW);
```

También se inicializa la comunicación serial:

```cpp
Serial.begin(9600);
```

### 11.3. Recepción de datos

Dentro de `loop()`, Arduino revisa continuamente si hay datos disponibles en el puerto serial. Si recibe el carácter `'1'`, enciende el LED de detección; si recibe `'0'`, enciende el LED de ausencia.

### 11.4. Apagado automático

El programa guarda el momento en que encendió un LED utilizando `millis()`. Luego, si han pasado cinco segundos, apaga ambos indicadores automáticamente. Esto evita que el circuito permanezca encendido de forma indefinida y proporciona una visualización temporal de cada evento.

### 11.5. Lógica de respuesta

La lógica implementada en Arduino es simple pero efectiva, ya que convierte la respuesta digital de la IA en una señal física inmediata. Esto demuestra cómo un sistema de software puede influir directamente sobre un entorno electrónico real.

---

## 12. Flujo completo de funcionamiento

El funcionamiento del sistema ocurre en una secuencia bien definida:

1. El usuario ejecuta el servidor MCP en Python.
2. El sistema detecta la cámara disponible.
3. Se captura una imagen en tiempo real.
4. La imagen se convierte a Base64.
5. La imagen se envía a LM Studio junto con la instrucción de análisis.
6. El modelo responde con un JSON estructurado.
7. Python interpreta la respuesta.
8. Si hay personas, se envía `'1'` a Arduino; si no hay personas, se envía `'0'`.
9. Arduino enciende el LED correspondiente.
10. Después de cinco segundos, ambos LEDs se apagan.

Este flujo refleja un sistema completo de percepción, análisis y actuación.

---

## 13. Resultados esperados

Se espera que el sistema sea capaz de:

* Detectar correctamente la presencia humana en una escena capturada por la cámara.
* Diferenciar entre escenarios con personas y sin personas.
* Generar descripciones breves y comprensibles del contenido visual.
* Activar correctamente los LEDs según el análisis realizado.
* Mantener una comunicación estable entre Python y Arduino.
* Operar de manera local sin depender de servicios externos.

En términos generales, el proyecto demuestra que la integración entre visión artificial, IA local y hardware embebido puede realizarse de manera ordenada, eficiente y comprensible para fines académicos.

---

## 14. Conclusión

El desarrollo de este proyecto permitió integrar de forma práctica conocimientos de inteligencia artificial, programación en Python, visión artificial, comunicación serial y control de hardware mediante Arduino. La solución implementada demuestra que es posible construir un sistema funcional de análisis visual sin depender de servicios en la nube, aprovechando herramientas locales como LM Studio y servicios estructurados mediante MCP.

Asimismo, la incorporación de Arduino permitió llevar la respuesta del modelo de IA al plano físico, logrando una interacción tangible entre software y electrónica. Esta característica fortalece el valor académico del proyecto, ya que no solo se analiza una imagen, sino que también se genera una acción concreta a partir del resultado obtenido.

Finalmente, este trabajo representa una base sólida para futuras mejoras, como la detección de múltiples objetos, el uso de sensores adicionales, la incorporación de una interfaz gráfica o la ampliación del sistema hacia escenarios de seguridad inteligente y monitoreo automatizado.

---

## 15. Posibles mejoras futuras

* Integrar una interfaz gráfica para visualizar la cámara y el resultado del análisis.
* Añadir sensores adicionales para complementar la detección visual.
* Guardar registros de eventos detectados en una base de datos local.
* Implementar notificaciones automáticas cuando se detecten personas.
* Mejorar el protocolo de respuesta del modelo para aumentar la precisión del JSON.
* Expandir el sistema para reconocer más categorías de objetos o acciones.

---

## 16. Anexo técnico: fragmentos representativos de implementación

### 16.1. Endpoint local de LM Studio

```python
http://127.0.0.1:1234/v1/chat/completions
```

### 16.2. Comunicación serial con Arduino

```python
arduino = serial.Serial('COM3', 9600, timeout=1)
```

### 16.3. Inicio del servidor MCP

```python
if __name__ == "__main__":
    app.run()
```

### 16.4. Inicialización de Arduino

```cpp
void setup() {
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  Serial.begin(9600);
}
```

### 16.5. Lógica de encendido de LEDs

```cpp
if (c == '1') {
  digitalWrite(ledPin1, HIGH);
  digitalWrite(ledPin2, LOW);
}

if (c == '0') {
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, HIGH);
}
```

---

## 17. Referencias técnicas sugeridas

* OpenCV Documentation.
* Arduino Documentation.
* LM Studio Documentation.
* FastMCP Documentation.
* Python Requests Documentation.
* PySerial Documentation.

---

## 18. Observación final

Este documento fue elaborado para presentar de forma más completa, ordenada y profesional el funcionamiento del sistema, incluyendo la parte de hardware, la configuración de Arduino, la lógica de comunicación serial, la integración con MCP y la arquitectura general del proyecto.
