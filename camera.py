import cv2 as cv
#### original opencv camera code ####
print( cv.__version__ )

def function():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        windowWidth=frame.shape[1]
        windowHeight=frame.shape[0]
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)    
        # apply a Gaussian blur to the image then find the brightest region
        gray = cv.GaussianBlur(gray, (11,11), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
        cv.circle(frame, maxLoc, 10, (255, 0, 0), 2)
        print(maxLoc)
        return(maxLoc, windowWidth, windowHeight)
        # Display the resulting frame
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()