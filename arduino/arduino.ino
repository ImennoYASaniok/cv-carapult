void setup() {
  Serial.begin(9600);
  pinMode(11, OUTPUT);
}


void loop() {
  if (Serial.available() > 0) {
  analogWrite(11, Serial.read());
  }
}

// void setup(){
// pinMode(6, OUTPUT);
// pinMode(7, OUTPUT);
// }

// void shoot(){
//   digitalWrite(7, HIGH);
//   analogWrite(6, 255);
// }

// void loop(){
//   //disable standby to make the motors run
//   shoot();
//   delay(1000);
// }
