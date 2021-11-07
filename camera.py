import cv2 as cv
import time
#### original opencv camera code ####

class Camera(object):
    def __init__(self):
        self.points = []
        self.brightest 
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
    
    def getPoint(self):
        pass

    def getLine(self):
        pass


cap = cv.VideoCapture(0, cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv.flip(frame, 1, frame)
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
    if maxVal > 180: print(maxLoc)
    else: print(-1,-1)
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

