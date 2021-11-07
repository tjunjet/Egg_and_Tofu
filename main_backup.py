WIDTH = 1200
HEIGHT = 800
CURSORLISTLENGTH = 10
CURSORMAXVELOCITY = 50
CURSORRANUM = 5

from cmu_112_graphics import *
import videoInput as vi
import cv2 as cv
import statistics

# Version 1: Use velocity and acceleration
def updateCursor(app):
    # Get data from videoInput
    inputData = vi.getPoint(app.cap)
    cursorNew = convertPoint(app, inputData[0], inputData[1])
    if len(app.cursorQueue) == 0:
        cursorPrev = (app.width // 2, app.height // 2)
    else:
        cursorPrev = app.cursorQueue[-1]
    app.cursorAccel = (cursorNew[0] - cursorPrev[0], cursorNew[1] - cursorPrev[1])
    if getMagnitude(*app.cursorAccel) < 200:
        app.cursor = cursorNew
    else:
        app.cursorVelocity = (app.cursorVelocity[0] + app.cursorAccel[0],
                              app.cursorVelocity[1] + app.cursorAccel[1])
        constrainVelocity(app, CURSORMAXVELOCITY)
        app.cursor = (cursorPrev[0] + app.cursorVelocity[0], cursorPrev[1] + app.cursorVelocity[1])
    app.cursorQueue.append(app.cursor)
    while len(app.cursorQueue) > CURSORLISTLENGTH:
        app.cursorQueue.pop(0)
    app.cursorCount += 1

# Version 2: Use running average
def updateCursor(app):
    # Get data from videoInput
    inputData = vi.getPoint(app.cap)
    cursorNew = convertPoint(app, inputData[0], inputData[1])
    app.cursorQueueRaw.append(cursorNew)
    while len(app.cursorQueueRaw) > CURSORRANUM:
        app.cursorQueueRaw.pop(0)
    if len(app.cursorQueueRaw) < CURSORRANUM:
        app.cursorQueue.append(cursorNew)
    else:
        cursorRAx = statistics.mean([point[0] for point in app.cursorQueueRaw])
        cursorRAy = statistics.mean([point[1] for point in app.cursorQueueRaw])
        cursorRA = (cursorRAx, cursorRAy)
        app.cursorQueue.append(cursorRA)
    while len(app.cursorQueue) > CURSORLISTLENGTH:
        app.cursorQueue.pop(0)
    app.cursorCount += 1

def getMagnitude(x, y):
    return (x ** 2 + y ** 2) ** 0.5

def constrainVelocity(app, maxSpeed):
    vx, vy = app.cursorVelocity
    speed = (vx ** 2 + vy ** 2) ** 0.5
    if speed > maxSpeed:
        vx = vx * (maxSpeed / speed)
        vy = vy * (maxSpeed / speed)
    app.cursorVelocity = (vx, vy)

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
    app.cursorVelocity = (0, 0)
    app.cursorAccel = (0, 0)
    app.cursorQueue = []
    app.cursorCount = 0
    app.cap = cv.VideoCapture(0)
    app.cursorQueueRaw = []
    app.timerDelay = 10

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
        canvas.create_line(*app.cursorQueue[i], *app.cursorQueue[i + 1], width = 10)
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