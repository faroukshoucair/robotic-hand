// Requires: "Adafruit PWM Servo Driver Library"

// Receive data from python script in the format: thumb,index,middle,ring,pinky\n

/*
5 Servos:
1. MG996R, controls the bend of robots thumb
2. MG996R, controls the bend of robots index
3. MG996R, controls the bend of robots middle finger
4. MG996R, controls the bend of robots ring and pinky fingers
5. SG90, controls the rotation of the robots thumb
*/


#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca;

//dummy test values until calibrated
//CHannel:               0     1    2    3   4
const int OPEN_DEG[5] = {165, 165, 165, 165, 165};  //Thumb, index, middle, ring + pinky, thumb rotation
const int CLOSED_DEG[5] = {70, 70, 70, 70, 110};

void setup() {
  Serial.begin(115200); // Standard baud rate for arduino uno

  pca.begin();
  pca.setOscillatorFrequency(27000000); //(from library instructions)
  pca.setPWMFreq(50); // Analog servos run at ~50 Hz updates (from library instructions)

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

    int channelValue[5] = {0};
    channelValue[0] = bendPercents[0]; //Robots thumb corresponds to thumb finger bend percentage
    channelValue[1] = bendPercents[1]; //Robots index corresponds to index finger bend percentage
    channelValue[2] = bendPercents[2]; //Robots middle corresponds to middle finger bend percentage
    channelValue[3] = (bendPercents[3] + bendPercents[4]) / 2; //Robots ring and pinky corresponds to the averge of the ring and pinky fingers bend percenteges
    channelValue[4] = bendPercents[0]; //Robots thumb rotation follows the thumb bend percentage

    for(int i = 0; i < 5; i++){
      int value = constrain(channelValue[i], 0, 100); // safety check to avoid servo yanking hard in one direction 
      int bendDegree = map(value, 0, 100, OPEN_DEG[i], CLOSED_DEG[i]); // Maps 0-100 bend percentage to degrees used by servo
      int pulse = map(bendDegree, 0, 180, 544, 2400); // Maps robots finger bend degree to pulse length to be used by PCA board
      pca.writeMicroseconds(i, pulse);
    }
    

  }

}
