const int ledPin1 = 13; // personas detectadas
const int ledPin2 = 8; // no hay personas

unsigned long ledOnTime = 0;
bool ledState = false;

void setup() {
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);

  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);

  Serial.begin(9600);
}

void loop() {

  if (Serial.available()) {
    char c = Serial.read();

    if (c == '1') {
      // persona detectada
      digitalWrite(ledPin1, HIGH);
      digitalWrite(ledPin2, LOW);

      ledState = true;
      ledOnTime = millis();

      Serial.println("PERSON DETECTED (LED1 ON)");
    }

    if (c == '0') {
      // no persona
      digitalWrite(ledPin1, LOW);
      digitalWrite(ledPin2, HIGH);

      ledState = true;
      ledOnTime = millis();

      Serial.println("NO PERSON (LED2 ON)");
    }
  }

  // apagar después de 5 segundos (ambos)
  if (ledState && (millis() - ledOnTime >= 5000)) {
    digitalWrite(ledPin1, LOW);
    digitalWrite(ledPin2, LOW);

    ledState = false;

    Serial.println("ALL LED OFF");
  }
}