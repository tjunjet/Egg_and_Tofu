WIDTH = 1000
HEIGHT = 1000
CURSOR_LIST_LENGTH = 10
CURSOR_RA_NUM = 5
CALIBRATION_RECTANGLE_TEMP = [0, 640, 0, 480] # TEMP
EGG_SPEED = 6
TOFU_SPEED = 8
STARTING_LIVES = 1000
G = 0.15

from cmu_112_graphics import *
import videoInput as vi
import fpsmeter
import cv2 as cv
import statistics, bpm_detection, shapes, time

# --------------------
# OPENCV FUNCTIONS
# --------------------

# Version 2: Use running average
def updateCursor(app):
    # Get data from videoInput
    inputData = vi.getPoint(app.cap)
    if inputData == None:
        return
    cursorNew = convertPoint(app, inputData[0], inputData[1])
    # app.cursurQueueRaw stores a queue of the CURSOR_RA_NUM most recent points
    app.cursorQueueRaw.append(cursorNew)
    # Ensure that a max of CURSOR_RA_NUM points is queued in app.cursorQueueRaw
    while len(app.cursorQueueRaw) > CURSOR_RA_NUM:
        app.cursorQueueRaw.pop(0)
    # If app.cursorQueueRaw doesn't have enough points to average (at the beginning of app), use raw points
    # Otherwise, average the CURSOR_RA_NUM most recent raw points, and append to app.cursorQueue
    if len(app.cursorQueueRaw) < CURSOR_RA_NUM:
        app.cursorQueue.append(cursorNew)
    else:
        cursorRAx = statistics.mean([point[0] for point in app.cursorQueueRaw])
        cursorRAy = statistics.mean([point[1] for point in app.cursorQueueRaw])
        cursorRA = (cursorRAx, cursorRAy)
        app.cursorQueue.append(cursorRA)
    # Ensure that a max of CURSOR_LIST_LENGTH points is queued in app.cursorQueue
    while len(app.cursorQueue) > CURSOR_LIST_LENGTH:
        app.cursorQueue.pop(0)
    # Increment app.cursorCount (for debugging/reference purposes)
    app.cursorCount += 1

# Helper function
# Takes in OpenCV coordinates, and converts to app window coordinates based on app.calibrationRectangle
def convertPoint(app, inputX, inputY):
    x = (inputX - app.calibrationRectangle[0])/(app.calibrationRectangle[1] - app.calibrationRectangle[0]) * app.width
    y = (inputY - app.calibrationRectangle[2])/(app.calibrationRectangle[3] - app.calibrationRectangle[2]) * app.height
    return x, y

# --------------------
# EGG & TOFU FUNCTIONS
# --------------------

def changeSlice(app):
    if len(app.cursorQueue) > 1:
        for i in range(len(app.cursorQueue)-1):
            p1 = shapes.Point(*app.cursorQueue[i])
            p2 = shapes.Point(*app.cursorQueue[i+1])
            for egg in app.eggs:
                egg.sliced(p1, p2)
            for tofu in app.tofus:
                tofu.sliced(p1,p2)

def createEgg(app):
    egg1 = shapes.Egg('Image/Egg.png', app.image1_width, app.image1_height)
    app.eggs.append(egg1)

def createTofu(app):
    tofu1 = shapes.Tofu('Image/Egg.png', app.image2_width, app.image2_height)
    app.tofus.append(tofu1)

def moveTofu(app):
    for tofu in app.tofus:
        tofu.y += TOFU_SPEED * (1 + tofu.counter * G)
        tofu.counter += 1

def moveEgg(app):
    for egg in app.eggs:
        egg.y += EGG_SPEED * (1 + egg.counter * G)
        egg.counter += 1

def moveBrokenEgg(app):
    for broken in app.brokeneggs:
        broken[1] += EGG_SPEED*5
        if broken[1] >= app.height:
            app.brokeneggs.remove(broken)

def removeEgg(app):
    i = 0
    while i < len(app.eggs):
        if app.eggs[i].y >= app.height:
            app.brokeneggs.append([app.eggs[i].x, app.eggs[i].y])
            app.eggs.pop(i)
            app.lives -= 1
        elif app.eggs[i].slice == True:
            app.score += app.eggs[i].points
            app.brokeneggs.append([app.eggs[i].x, app.eggs[i].y])
            app.eggs.pop(i)
        else:
            i += 1

def removeTofu(app):
    i = 0
    while i < len(app.tofus):
        if app.tofus[i].y >= app.height:
            app.tofus.pop(i)
            app.lives -= 1
        elif app.tofus[i].slice == True:
            app.score += app.tofus[i].points
            app.tofus.pop(i)
        else:
            i += 1

# --------------------
# MUSIC PROCESSING FUNCTIONS
# --------------------

def getBPM(app, filename):
    return bpm_detection.main(app.filename)

# --------------------
# APP STARTED
# --------------------

def appStarted(app):
    app.mode = "gameMode"
    app.calibrationRectangle = CALIBRATION_RECTANGLE_TEMP
    app.cursor = (0, 0)
    app.cursorQueue = []
    app.cursorQueueRaw = []
    app.cursorCount = 0
    app.cap = cv.VideoCapture(0)
    app.fpsmeter = fpsmeter.FPSmeter()
    app.score = 0
    app.lives = STARTING_LIVES
    app.isGameOver = False
    graphicsparams(app)

def graphicsparams(app):
    ###########################################################
    app.image1 = app.loadImage(r"Image/Egg.png")
    app.image1_scale = app.scaleImage(app.image1, 2/9)
    app.image1_width, app.image1_height = app.image1_scale.size
    ###########################################################
    ###########################################################
    app.image2 = app.loadImage(r"Image/Tofu.png")
    app.image2_scale = app.scaleImage(app.image2, 3/9)
    app.image2_width, app.image2_height = app.image2_scale.size
    ###########################################################
    ###########################################################
    #https://www.deviantart.com/jaywlng/art/Tofu-301528003
    app.background = app.loadImage(r"Image/Background.png")
    ###########################################################
    #https://www.pngkey.com/maxpic/u2e6y3i1q8r5u2e6/
    #broken egg
    app.brokenegg = app.loadImage(r"Image/brokenegg.png")
    app.brokenegg_scale = app.scaleImage(app.brokenegg, 2/9)
    ###########################################################
    app.filename = "Music/Forever Bound - Stereo Madness.wav"
    app.bpm = getBPM(app, app.filename)
    # Time interval between successive item drops
    app.period = (60 / app.bpm)
    app.timerDelay = 1
    app.timeElapsed = 0
    app.startTime = time.time()

    app.eggs = []
    #list of tuples containing x,y coordinate of broken egg
    app.brokeneggs = []
    app.tofus = []
    app.counter = 0

# --------------------
# GAME MODE
# --------------------

def gameMode_timerFired(app):
    if app.lives < 0:
        app.isGameOver = True
    if app.isGameOver == True:
        return
    updateCursor(app)

    print(app.cursorCount, app.cursorQueue)
    app.fpsmeter.addFrame()

    newTime = time.time()
    timePassed = newTime - app.startTime
    # app.timerDelay
    # app.timeElapsed += app.timerDelay
    if timePassed > app.period:
        createEgg(app)
        createTofu(app)
        app.startTime = newTime
    moveEgg(app)
    moveTofu(app)
    changeSlice(app)
    removeEgg(app)
    removeTofu(app)
    moveBrokenEgg(app)

def gameMode_redrawAll(app, canvas):
    if app.isGameOver == True:
        drawGameOver(app, canvas)
        return
    canvas.create_text(app.width//2, app.height//2, text = "Calibration Mode")
    drawBackground(app, canvas)
    drawEgg(app, canvas)
    drawTofu(app, canvas)
    drawBrokenEgg(app,canvas)
    for i in range(len(app.cursorQueue) - 1):
        canvas.create_line(*app.cursorQueue[i], *app.cursorQueue[i + 1], width = 10)
    canvas.create_text(app.width//2, app.height * 0.75, text = f"FPS: {round(app.fpsmeter.getFPS())}")
    canvas.create_text(app.width//2, app.height//10, font = "Arial 20", text = f"SCORE: {app.score}     LIVES: {app.lives}")

# --------------------
# DRAWING
# --------------------

def drawGameOver(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "red")
    canvas.create_text(app.width//2, app.height//2, text = "Game Over", font = "Arial 50", fill = "yellow")

def drawBackground(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))

def drawBrokenEgg(app,canvas):
    if app.brokeneggs != []:
        for x, y in app.brokeneggs:
            canvas.create_image(x, y, image=ImageTk.PhotoImage(app.brokenegg_scale))

def drawEgg(app, canvas):
    if app.eggs != []:
        for egg in app.eggs:
            canvas.create_image(egg.x, egg.y, image=ImageTk.PhotoImage(app.image1_scale))
    
def drawTofu(app, canvas):
    if app.tofus != []:
        for tofu in app.tofus:
            canvas.create_image(tofu.x, tofu.y, image=ImageTk.PhotoImage(app.image2_scale))

runApp(width = WIDTH, height = HEIGHT)

