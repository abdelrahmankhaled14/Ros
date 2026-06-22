#define TRIG_PIN 9
#define ECHO_PIN 10
#define POT_PIN A0

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // --- HC-SR04 ---
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30 ms timeout
  float distance_m = 0.0;
  if (duration > 0) {
    distance_m = (duration * 0.0343) / 2.0 / 100.0; // cm -> m
  }

  // --- Potentiometer (0–2.0 m) ---
  int pot_raw = analogRead(POT_PIN);
  float threshold_m = (pot_raw / 1023.0) * 2.0;

  // --- Serial Protocol: U:<dist>,P:<thresh> ---
  Serial.print("U:");
  Serial.print(distance_m, 3);
  Serial.print(",P:");
  Serial.println(threshold_m, 3);

  delay(100); // 10 Hz
}