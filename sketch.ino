const int buttonPin = D2;

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.println("Wokwi button demo started");
}

void loop() {
  if (digitalRead(buttonPin) == LOW) {
    Serial.println("Button pressed");
  } else {
    Serial.println("Button released");
  }
  delay(200);
}
