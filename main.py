import cv2 # import opencv
import mediapipe as mp
import time

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

        result = detector.detect_for_video(mp_image, timestamp_ms)

        # display frame
        cv2.imshow("Robot hand tracker", frame)

        # render frame/image and check for exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # close camera window   
    cam.release()
    detector.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()