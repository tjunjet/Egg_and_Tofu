import cv2 as cv

print( cv.__version__ )

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
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Converts the grayscale image to black and white
    # https://techtutorialsx.com/2019/04/13/python-opencv-converting-image-to-black-and-white/
    #(thresh, blackAndWhiteImage) = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    #(minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    #cv.circle(frame, maxLoc, 5, (255, 0, 0), 2)
    
    # apply a Gaussian blur to the image then find the brightest region
    gray = cv.GaussianBlur(gray, (11,11), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    cv.circle(frame, maxLoc, 10, (255, 0, 0), 2)
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()