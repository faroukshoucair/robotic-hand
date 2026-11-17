
// Receive data from python script in the format: thumb,index,middle,ring,pinky\n

#include <Servo.h>

Servo servo;

void setup() {
  Serial.begin(115200); // Standard baud rate for arduino uno
  servo.attach(10);
  Serial.println("ready");

}

void loop() {
  
  // Serial.available = 0 ==> no data received
  if(Serial.available() > 0){
    String line = Serial.readStringUntil("\n");

    Serial.println("Data: " + line);

  }

}
