# PLACEHOLDER VARIABLES
# Calibration (4 points at the beginning)
# p1 to p4 from top-left corner (on screen POV), clockwise
p1 = (20, 20)
p2 = (390, 20)
p3 = (390, 390)
p4 = (20, 390)
# Data constantly piped in from OpenCV
inputPoint = (200, 200)

WIDTH = 1200
HEIGHT = 800

from cmu_112_graphics import *
import videoInput as vi

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

def convertPoint(app, inputX, inputY):
    x = None
    y = None #
    return x, y

def appStarted(app):
    app.mode = "calibrationMode"
    # app.inputXmin, app.inputXmax, app.inputYmin, app.inputYmax = getRangeRectangle(p1, p2, p3, p4)

def calibrationMode_timerFired(app):
    app.inputX, app.inputY, app.inputWidth, app.inputHeight = vi.getPoint()
    app.cursorX = (app.width / app.inputWidth) * app.inputX
    app.cursorY = (app.height / app.inputHeight) * app.inputY

def gameMode_timerFired(app):


def calibrationMode_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text = "calib mode")
    canvas.create_oval(app.cursorX, app.cursorY, r = 10, fill = red)
    pass

def gameMode_redrawAll(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text="game mode")
    pass

runApp(width = WIDTH, height = HEIGHT)