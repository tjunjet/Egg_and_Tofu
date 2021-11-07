calibrationRectangleTemp = [0, 640, 0, 480]

WIDTH = 1200
HEIGHT = 800

from cmu_112_graphics import *
import videoInput as vi

"""
def getRangeRectangle(*args):
    if len(args) != 4:
        print(f"4 points expected; {len(args)} given!")
        return None
    topLeft, topRight, bottomRight, bottomLeft = args
    inputXmin = max([topLeft[0],     bottomLeft[0]])
    inputXmax = min([topRight[0],    bottomRight[0]])
    inputYmin = max([topLeft[1],     topRight[1]])
    inputYmax = min([bottomLeft[1],  bottomRight[1]])
    return inputXmin, inputXmax, inputYmin, inputYmax
"""

# Takes in OpenCV coordinates, and converts to app window coordinates based on app.calibrationRectangle
def convertPoint(app, inputX, inputY):
    x = (inputX - app.calibrationRectangle[0])/(app.calibrationRectangle[1] - app.calibrationRectangle[0]) * app.width
    y = (inputY - app.calibrationRectangle[2])/(app.calibrationRectangle[3] - app.calibrationRectangle[2]) * app.height
    return x, y

def updateCursor(app):
    inputData = vi.getPoint()
    app.cursor = convertPoint(app, inputData[0], inputData[1])

def appStarted(app):
    app.mode = "calibrationMode"
    app.calibrationRectangle = calibrationRectangleTemp
    app.cursor = (0, 0)

def calibrationMode_timerFired(app):
    updateCursor(app)
    print("test")

def gameMode_timerFired(app):
    pass

def calibrationMode_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text = "calib mode")
    canvas.create_oval(app.cursor[0] - 5, app.cursor[1] - 5, app.cursor[0] + 5, app.cursor[1] + 5, fill = "red")
    pass

def gameMode_redrawAll(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text="game mode")
    pass

runApp(width = WIDTH, height = HEIGHT)

# data = vi.getPoint()
# print(data)