import cv2 # import opencv
import mediapipe as mp
import time
import numpy as np

# Hand landmark model

# ID	Landmark	    ID	Landmark
# 0	WRIST	            11	MIDDLE_FINGER_DIP
# 1	THUMB_CMC	        12	MIDDLE_FINGER_TIP
# 2	THUMB_MCP	        13	RING_FINGER_MCP
# 3	THUMB_IP	        14	RING_FINGER_PIP
# 4	THUMB_TIP	        15	RING_FINGER_DIP
# 5	INDEX_FINGER_MCP	16	RING_FINGER_TIP
# 6	INDEX_FINGER_PIP	17	PINKY_MCP
# 7	INDEX_FINGER_DIP	18	PINKY_PIP
# 8	INDEX_FINGER_TIP	19	PINKY_DIP
# 9	MIDDLE_FINGER_MCP	20	PINKY_TIP
# 10 MIDDLE_FINGER_PIP		



BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# settings for hand detector
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)


def main():

    # connects to defaults laptop camera 
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: could not open camera")
        return

    # creates the hand detector
    detector = HandLandmarker.create_from_options(options)

    start_time = time.time()


    while True:

        # read frame and verify its working
        check, frame = cam.read() 
        if not check:
            print("Failed to read frame")
            break

        # mirror frame
        frame = cv2.flip(frame, 1)

        # Opencv -> BGR
        # MediaPipe -> RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        timestamp_ms = round(((time.time() - start_time) * 1000))

        # detect 21 landmarks on hand
        # returns a list of list of 21 handmarks on each hand
        result = detector.detect_for_video(mp_image, timestamp_ms)

        # Draw 21 landmarks on hand if detected
        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            drawLandmarks = mp.tasks.vision.drawing_utils.draw_landmarks
            HAND_CONNECTIONS = mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS
            drawLandmarks(frame, hand, HAND_CONNECTIONS)



        # display frame
        cv2.imshow("Robot hand tracker", frame)

        # render frame/image and check for exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # close camera window, stop hand detection, close camera
    cam.release()
    detector.close()
    cv2.destroyAllWindows()


# measures the angle in degrees between two bones
def angle(bone1, bone2):
    dot_prod = np.dot(bone1, bone2)
    len_bone1 = np.linalg.norm(bone1)
    len_bone2 = np.linalg.norm(bone2)

    # safety check: zero-length vector has no angle
    if len_bone2 == 0 or len_bone2 == 0:
        return 0.0

    cos_theta = dot_prod / (len_bone1 * len_bone2)

    # forces cos_theta to be b/t -1 and 1 to avoid rounding errors
    cos_theta = np.clip(cos_theta, -1, 1) 

    theta_deg = np.degrees(np.arccos(cos_theta))
    return theta_deg

if __name__ == "__main__":
    main()