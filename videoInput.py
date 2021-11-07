import cv2 as cv

def getPoint(cap):
    # When called, return coordinates of bright point on webcam
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame=cv.flip(frame,1,frame)
    # if frame is read correctly ret is True
    if ret:
        # height, width of camera screen
        width=frame.shape[1]
        height=frame.shape[0]
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)    
        # apply a Gaussian blur to the image then find the brightest region
        gray = cv.GaussianBlur(gray, (11,11), 0)
        (_, maxVal, _, maxLoc) = cv.minMaxLoc(gray)
        # cv.circle(frame, maxLoc, 10, (255, 0, 0), 2)
        if maxVal > 180: 
            x, y = maxLoc 
            return x, y, width, height
        else: 
            return None
        # cv.imshow('frame', frame)
        # cv.waitKey(5000)
        # cv.destroyAllWindows()
        

