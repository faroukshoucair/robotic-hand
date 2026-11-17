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
    String line = Serial.readStringUntil('\n');

    Serial.println("Data: " + line);

    int bendPercents[5] = {0};

    int firstComma = line.indexOf(","); // First comma's position
    int secondComma = line.indexOf(",", firstComma+1); // Second comma's position
    int thirdComma = line.indexOf(",", secondComma+1); // Third comma's position
    int fourthComma = line.indexOf(",", thirdComma+1); // Fourth comma's position

    // Incomplete data, can cause sudden jerks without check
    if(fourthComma == -1){
      Serial.println("Incomplete data received");
      return;
    }

    bendPercents[0] = line.substring(0, firstComma).toInt(); //Thumb
    bendPercents[1] = line.substring(firstComma+1, secondComma).toInt(); //Index
    bendPercents[2] = line.substring(secondComma+1, thirdComma).toInt(); //Middle
    bendPercents[3] = line.substring(thirdComma+1, fourthComma).toInt(); //Ring
    bendPercents[4] = line.substring(fourthComma+1, line.length()).toInt(); //Pinky

    Serial.print(String("T: ") + bendPercents[0] + " ");
    Serial.print(String("I: ") + bendPercents[1] + " ");
    Serial.print(String("M: ") + bendPercents[2] + " ");
    Serial.print(String("R: ") + bendPercents[3] + " ");
    Serial.println(String("P: ") + bendPercents[4]);

    // Maps 0-100 bend percentage to servo's 0-180 degrees
    int angle = map(bendPercents[1], 0, 100, 0, 180);
    servo.write(angle);
    

  }

}
