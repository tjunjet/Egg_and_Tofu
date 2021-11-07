WIDTH = 1200
HEIGHT = 800
CURSORLISTLENGTH = 10

from cmu_112_graphics import *
import videoInput as vi
import cv2 as cv

def updateCursor(app):
    # Get data from videoInput
    inputData = vi.getPoint(app.cap)
    app.cursor = convertPoint(app, inputData[0], inputData[1])
    app.cursorQueue.append(app.cursor)
    while len(app.cursorQueue) > CURSORLISTLENGTH:
        app.cursorQueue.pop(0)
    app.cursorCount += 1

# Takes in OpenCV coordinates, and converts to app window coordinates based on app.calibrationRectangle
calibrationRectangleTemp = [0, 640, 0, 480] # TEMP
def convertPoint(app, inputX, inputY):
    x = (inputX - app.calibrationRectangle[0])/(app.calibrationRectangle[1] - app.calibrationRectangle[0]) * app.width
    y = (inputY - app.calibrationRectangle[2])/(app.calibrationRectangle[3] - app.calibrationRectangle[2]) * app.height
    return x, y

# --------------------
# APP STARTED
# --------------------

def appStarted(app):
    app.mode = "calibrationMode"
    app.calibrationRectangle = calibrationRectangleTemp
    app.cursor = (0, 0)
    app.cursorQueue = []
    app.cursorCount = 0
    app.cap = cv.VideoCapture(0)

# --------------------
# CALIBRATION MODE
# --------------------

def calibrationMode_timerFired(app):
    updateCursor(app)
    print(app.cursorCount, app.cursorQueue)

def calibrationMode_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text = "calib mode")
    # canvas.create_oval(app.cursor[0] - 5, app.cursor[1] - 5, app.cursor[0] + 5, app.cursor[1] + 5, fill = "red")
    for i in range(len(app.cursorQueue) - 1):
        canvas.create_line(*app.cursorQueue[i], *app.cursorQueue[i + 1])
    pass

# --------------------
# GAME MODE
# --------------------

def gameMode_timerFired(app):
    pass

def gameMode_redrawAll(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text="game mode")
    pass

runApp(width = WIDTH, height = HEIGHT)