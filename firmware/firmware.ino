/*
  fruit_sorter.ino — Firmware Arduino para VisionSystem

  Protocolo Serial (9600 baud):
  - Recibe '1' → Enciende LED blanco (persona detectada)
  - Recibe '0' → Enciende LED amarillo (sin persona)
  - Recibe 'PING' → Responde 'PONG'

  Requiere:
  - Arduino UNO (o compatible)
  - 2× LED con resistencias limitadoras
  - Pin 13: LED blanco (persona)
  - Pin 8: LED amarillo (sin persona)
  - Pin 9: TRIG del sensor ultrasónico
  - Pin 10: ECHO del sensor ultrasónico
*/

// Pines digitales para los LEDs
const int LED_PERSON = 13;  // LED blanco — persona detectada
const int LED_NO_PERSON = 8;  // LED amarillo — sin persona

// Pines del sensor ultrasónico HC-SR04
const int ULTRASONIC_TRIG = 9;
const int ULTRASONIC_ECHO = 10;

// Variables de control
unsigned long ledOnTime = 0;
const unsigned long LED_TIMEOUT = 5000;  // 5 segundos
boolean ledActive = false;

void setup() {
  // Configurar pines como salidas
  pinMode(LED_PERSON, OUTPUT);
  pinMode(LED_NO_PERSON, OUTPUT);
  pinMode(ULTRASONIC_TRIG, OUTPUT);
  pinMode(ULTRASONIC_ECHO, INPUT);

  // Apagar LEDs al inicio
  digitalWrite(LED_PERSON, LOW);
  digitalWrite(LED_NO_PERSON, LOW);

  // Inicializar comunicación serial
  Serial.begin(9600);
  delay(1000);

  // Mensaje de inicio
  Serial.println("READY");
}

float readDistanceCm() {
  digitalWrite(ULTRASONIC_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRASONIC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_TRIG, LOW);

  long duration = pulseIn(ULTRASONIC_ECHO, HIGH, 30000);
  if (duration == 0) {
    return -1.0;
  }

  float distanceCm = duration * 0.0343 / 2.0;
  return distanceCm;
}

void loop() {
  // Verificar si hay datos en el puerto serial
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Eliminar espacios en blanco

    // Procesar comando
    if (command == "1") {
      // Persona detectada — enciende LED blanco
      digitalWrite(LED_PERSON, HIGH);
      digitalWrite(LED_NO_PERSON, LOW);
      ledOnTime = millis();
      ledActive = true;
      Serial.println("OK");

    } else if (command == "0") {
      // Sin persona — enciende LED amarillo
      digitalWrite(LED_PERSON, LOW);
      digitalWrite(LED_NO_PERSON, HIGH);
      ledOnTime = millis();
      ledActive = true;
      Serial.println("OK");

    } else if (command == "PING") {
      // Verificación de conexión
      Serial.println("PONG");

    } else if (command == "DISTANCE") {
      float distance = readDistanceCm();
      if (distance < 0) {
        Serial.println("DISTANCE:ERROR");
      } else {
        Serial.print("DISTANCE:");
        Serial.println(distance, 1);
      }

    } else {
      // Comando no reconocido
      Serial.println("ERROR:UNKNOWN_COMMAND");
    }
  }

  // Apagar LEDs después del timeout
  if (ledActive && (millis() - ledOnTime) >= LED_TIMEOUT) {
    digitalWrite(LED_PERSON, LOW);
    digitalWrite(LED_NO_PERSON, LOW);
    ledActive = false;
  }
}
