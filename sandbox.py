WIDTH = 1000
HEIGHT = 1000
CURSOR_LIST_LENGTH = 10
CURSOR_RA_NUM = 5
CALIBRATION_RECTANGLE_TEMP = [0, 640, 0, 480] # TEMP
EGG_SPEED = 5
TOFU_SPEED = 7
STARTING_LIVES = float("inf")
G = 0.15
IS_VERBOSE = False

from cmu_112_graphics import *
import videoInput as vi
import fpsmeter
import cv2 as cv
import statistics, bpm_detection, shapes, time, random
import sound
import pygame

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

def moveBrokenTofu(app):
    for broken in app.brokentofus:
        broken[1] += TOFU_SPEED*5
        if broken[1] >= app.height:
            app.brokentofus.remove(broken)

def removeEgg(app):
    i = 0
    while i < len(app.eggs):
        if app.eggs[i].y >= app.height:
            app.brokeneggs.append([app.eggs[i].x, app.eggs[i].y])
            app.eggs.pop(i)
            app.lives -= 1
            app.combo = 0
        elif app.eggs[i].slice == True:
            app.score += app.eggs[i].points
            app.brokeneggs.append([app.eggs[i].x, app.eggs[i].y])
            app.eggs.pop(i)
            app.hits += 1
            app.combo += 1
        else:
            i += 1

def removeTofu(app):
    i = 0
    while i < len(app.tofus):
        if app.tofus[i].y >= app.height:
            app.brokentofus.append([app.tofus[i].x, app.tofus[i].y])
            app.tofus.pop(i)
            app.lives -= 1
            app.combo = 0
        elif app.tofus[i].slice == True:
            app.brokentofus.append([app.tofus[i].x, app.tofus[i].y])
            app.score += app.tofus[i].points
            app.tofus.pop(i)
            app.hits += 1
            app.combo += 1
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
    app.counter = 0
    app.hits = 0
    app.percentage = 0
    app.isFlashing = False
    soundParams(app)
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
    app.background_trans = app.background.transpose(Image.FLIP_LEFT_RIGHT)
    ###########################################################
    #https://www.pngkey.com/maxpic/u2e6y3i1q8r5u2e6/
    #broken egg
    app.brokenegg = app.loadImage(r"Image/brokenegg.png")
    app.brokenegg_scale = app.scaleImage(app.brokenegg, 2/9)
    ###########################################################
    #broken tofu
    app.brokentofu = app.loadImage(r"Image/brokentofu.png")
    app.brokentofu_scale = app.scaleImage(app.brokentofu, 2/9)
    ###########################################################
    app.combo = 0
    app.eggs = []

    #list of list containing x,y coordinate of broken egg
    app.brokeneggs = []

    app.tofus = []
    #list of list containing x,y coord of broken tofu
    app.brokentofus = []
    app.counter = 0
    app.backBool = True

def returninput(app):
    while True:
        try:
            app.userinput = input('''
            Enter 0 or 1 or 2 to choose your song:

            0: Stereo Madness
            1: Moonlight Sonata (1st Movement)
            2: Nocturne op.9 No.2

            ''')
            x = int(app.userinput)
            if 0 <= x <= len(app.songs) - 1:
                return x
        except:
            print("INVALID INPUT!!!!")
            continue


def soundParams(app):
    app.songs = {
    #from https://www.youtube.com/watch?v=JhKyKEDxo8Q
    0 : "Music/Forever Bound - Stereo Madness.wav",
    #from https://www.youtube.com/watch?v=nT7_IZPHHb0
    1 : "Music/Beethoven - Moonlight Sonata (1st Movement).wav",
    #from https://www.youtube.com/watch?v=9E6b3swbnWg
    2 : 'Music/Chopin - Nocturne op.9 No.2.wav'
    }   
    app.filename = app.songs[returninput(app)]
    pygame.mixer.init()
    app.sound = sound.Sound(app.filename)
    app.sound.start()
    app.bpm = getBPM(app, app.filename)
    # Time interval between successive item drops
    app.period = (60 / app.bpm)
    app.timerDelay = 1
    app.timeElapsed = 0
    app.startTime = time.time()
    

# --------------------
# GAME MODE
# --------------------

def gameMode_timerFired(app):
    if app.lives < 0:
        app.isGameOver = True
    if app.isGameOver == True:
        return
    updateCursor(app)

    if IS_VERBOSE:
        print(app.cursorCount, app.cursorQueue)
    app.fpsmeter.addFrame()

    newTime = time.time()
    timePassed = newTime - app.startTime
    # app.timerDelay
    # app.timeElapsed += app.timerDelay
    if timePassed > app.period:
        choice = random.randint(1, 6)
        if choice == 1:
            createTofu(app)
        else:
            createEgg(app)
        app.counter += 1
        app.startTime = newTime
        app.isFlashing = True
        app.backBool = not app.backBool
    else:
        app.isFlashing = False
    try:
        app.percentage = round(100 * app.hits/app.counter)
    except:
        pass
    moveEgg(app)
    moveTofu(app)
    changeSlice(app)
    removeEgg(app)
    removeTofu(app)
    moveBrokenEgg(app)
    moveBrokenTofu(app)
    if app.sound.isPlaying() == False:
        app.isGameOver = True

def gameMode_redrawAll(app, canvas):
    if app.isGameOver == True:
        drawGameOver(app, canvas)
        return
    canvas.create_text(app.width//2, app.height//2, text = "Calibration Mode")
    drawBackground(app, canvas)
    drawEgg(app, canvas)
    drawTofu(app, canvas)
    drawBrokenEgg(app,canvas)
    drawBrokenTofu(app,canvas)
    drawInstructions(app, canvas)
    r = 10
    if len(app.cursorQueue) > 0:
        canvas.create_oval(app.cursorQueue[-1][0] - r, app.cursorQueue[-1][1] - r, app.cursorQueue[-1][0] + r, app.cursorQueue[-1][1] + r, width = 5, fill = "white")
    for i in range(len(app.cursorQueue) - 1):
        canvas.create_line(*app.cursorQueue[i], *app.cursorQueue[i + 1], width = 5)
    canvas.create_text(app.width//2, app.height * 0.75, text = f"FPS: {round(app.fpsmeter.getFPS())}")
    canvas.create_text(app.width//2, app.height//10, font = "Arial 20", text = f"SCORE: {app.score}     COMBO: {app.combo}     HITS: {app.percentage}%")


# --------------------
# DRAWING
# --------------------

def drawGameOver(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "red")
    canvas.create_text(app.width//2, app.height//2, text = "Game Over", font = "Arial 50", fill = "yellow")
    canvas.create_text(app.width//2, app.height * 0.75, text = f"Percentage hit: {round(100 * app.hits/app.counter)}%", font = "Arial 60")

def drawBackground(app, canvas):
    #if app.isFlashing == False:
    if app.backBool == True:
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))
    elif app.backBool == False:
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background_trans))
    #else:
        #canvas.create_rectangle(0, 0, app.width, app.height, fill = "white")

def drawBrokenTofu(app,canvas):
    if app.brokentofus != []:
        for x, y in app.brokentofus:
            canvas.create_image(x, y, image=ImageTk.PhotoImage(app.brokentofu_scale))

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

def drawInstructions(app, canvas):
    lineHeight = 22
    canvas.create_text(app.width//2, lineHeight*2, font = "Arial 15", text = "Slice eggs and tofu with your smartphone flashlight!")
    canvas.create_text(app.width//2, lineHeight*3, font = "Arial 15", text="Eggs = 10 points; Tofu = 50 points")

# --------------------
# CONTROLLER
# --------------------

def keyPressed(app, event):
    if (event.key == 's'):
        app.sound.start()
        print("YAY")
    elif (event.key == "r"):
        appStarted(app)


runApp(width = WIDTH, height = HEIGHT)