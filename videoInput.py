import cv2 as cv

def getPoint():
    # When called, return coordinates of bright point on webcam
    cap = cv.VideoCapture(1)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if ret:
        # height, width of camera screen
        width=frame.shape[1]
        height=frame.shape[0]
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)    
        # apply a Gaussian blur to the image then find the brightest region
        gray = cv.GaussianBlur(gray, (11,11), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
        cv.circle(frame, maxLoc, 10, (255, 0, 0), 2)
        x, y = maxLoc 
        cap.release()
        return x, y, width, height
    # Display the resulting frame
    # cv.imshow('frame', frame)
    # if cv.waitKey(1) == ord('q'):
    #     break
    # # When everything done, release the capture
    # cv.destroyAllWindows()
    

