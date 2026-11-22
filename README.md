# 5 actuated DOF Robotic Hand

3D-printed robotic hand that copies your hand movements in real time using a webcam, and recognizes how many fingers you're holding up.

## Demo
_Demo video coming soon._



## How it works
```
webcam → MediaPipe → bend angles → 0–100 per finger → USB serial → Arduino → PCA9685 (servo pulses) → servos
```

1. **Hand tracking.** Each webcam frame goes through Google's MediaPipe Hand Landmarker, which finds 21 landmarks on the hand (wrist, knuckles, joints, and fingertips).

2. **Measuring how bent each finger is.** For each finger, the landmarks are turned into bone vectors (one point to the next), and the angle between each pair of neighboring bones is measured with the dot product. Adding up a finger's joint angles gives its total bend. This uses MediaPipe's 3D world landmarks (real-world meters), so the measurement depends only on the shape of the hand, not its position, size in the frame, or rotation.

3. **Calibration.** Every finger has a different range: a straight index finger reads about 55° and a fist about 220°, while the thumb only moves between about 40° and 140°. Each finger's measured open and closed angles are used to map its bend to a common scale: 0 = fully open, 100 = fully closed.

4. **Finger counting.** A finger counts as "up" when its value is below a threshold (15). The count is drawn on the video in real time.

5. **Sending to the robot.** The five values are sent to the Arduino over USB serial at 115200 baud, one line per frame:
```
thumb,index,middle,ring,pinky\n
```

6. **Moving the robot hand.** The Arduino parses each line, ignores incomplete messages, constrains the values, and maps each one to its servo's calibrated open and closed angles. A PCA9685 board generates the servo signals in hardware, which keeps them steady while the Arduino handles serial data.

### Design choices
- Ring and pinky share one servo, so their two values are averaged.
- Thumb rotation follows the thumb's bend: as the thumb curls, it also swings across the palm, as it does in a fist.
- Each finger is pulled closed by a fishing-line tendon and pulled back open by shock cord.


## Hardware
| Part | Quantity |
|---|---|
| [3D printed hand](https://www.thingiverse.com/thing:2269115) | 1 |
| MG996R servo | 4 |
| SG90 micro servo | 1 |
| Arduino Uno | 1 |
| PCA9685 16-channel servo driver | 1 |
| 5 V 5 A power supply | 1 |
| 50 lb monofilament fishing line | ~2 m |
| 1/8" shock cord | ~3 m |

### Servo channels (PCA9685)
| Channel | Servo | Moves |
|---|---|---|
| 0 | MG996R | thumb bend |
| 1 | MG996R | index |
| 2 | MG996R | middle |
| 3 | MG996R | ring + pinky |
| 4 | SG90 | thumb rotation |

### Wiring
| Arduino Uno | PCA9685 |
|---|---|
| 5V | VCC |
| GND | GND |
| A4 | SDA |
| A5 | SCL |
 
- The 5 V power supply connects to the PCA9685's **screw terminal** (V+ and GND), not to the Uno!
- The Uno is powered over USB from the laptop.

## Setup & Installation
**Python**
```
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
curl -L -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

**Arduino**
1. In the Arduino IDE, install **Adafruit PWM Servo Driver Library** (Tools → Manage Libraries).
2. Open `arduino/hand_receiver/hand_receiver.ino` and upload it to the Uno.


**Run**
1. Find the Uno's port with `ls /dev/cu.*` and set `SERIAL_PORT` in `main.py` (also make sure the Arduino Uno is plugged in).
2. Ensure the Arduino Serial Monitor is closed (only one program can use the port).
3. Run:
```bash
python main.py
```
4. Hold up your **left** hand (the robot is a left hand). Press `q` in the video window to quit.


## Repo structure
 
```
robotic-hand/
├── main.py                          # hand tracking, finger counting, sends values to the Arduino
├── requirements.txt
├── arduino/
│   └── hand_receiver/
│       └── hand_receiver.ino        # receives values, drives the servos via the PCA9685
└── README.md
```

## Credits
- Hand design: [Humanoid Robotic Hand by grossrc](https://www.thingiverse.com/thing:2269115) on Thingiverse
- Hand tracking: [MediaPipe Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker)


## Future work
- Measure thumb rotation directly from the hand, so it moves independently of the thumb's bend
- Smoother, more human-like motion with easing on the Arduino
- Wireless control with an ESP32
- Recognizing more gestures than finger counts

