import cv2 #import opencv

def main():

    #connects to defaults laptop camera 
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Error: could not open camera")
        return

    while True:
        #read frame and verify its working
        check, frame = cam.read() 
        if not check:
            print("Failed to read frame")
            break

        #mirror and display frame
        frame = cv2.flip(frame, 1)
        cv2.imshow("Robot hand tracker", frame)

        #render frame/image and check for exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    #close camera window   
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()