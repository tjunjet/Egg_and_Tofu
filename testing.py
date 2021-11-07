from cmu_112_graphics import *
import bpm_detection
import shapes
import time 

#from
# http://clipart-library.com/free/egg-png-transparent.html
# https://genshin-impact.fandom.com/wiki/Almond_Tofu

# Model
def appStarted(app):
    app.image1 = app.loadImage(r"Image/Egg.png")
    app.image1_scale = app.scaleImage(app.image1, 2/9)
    app.image2 = app.loadImage(r"Image/Tofu.png")
    app.filename = "Music/Forever Bound - Stereo Madness.wav"
    app.bpm = getBPM(app, app.filename)
    # Time interval between successive item drops
    app.timerDelay = int((60 / app.bpm) * 1000)
    app.timeElapsed = 0
    app.eggs = []
    app.tofus = []
    app.counter = 0

def createEgg(app):
    egg1 = shapes.RedEgg('Image/Egg.png')
    app.eggs.append(egg1)

def moveEgg(app):
    for egg in app.eggs:
        egg.y += 100

# View
def drawBackground(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'red')

def drawEgg(app, canvas):
    if app.eggs != []:
        for egg in app.eggs:
            canvas.create_image(egg.x, egg.y, image=ImageTk.PhotoImage(app.image1_scale))
    
def drawTofu(app, canvas):
    canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.image2))

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawEgg(app, canvas)



# Controller

#def addEgg(app):
    # x = app.width/2
    # y = app.height/2
    # if len(app.eggs) == 0:
    #     app.eggs.append((x,y))

def removeEgg(app):
    app.eggs = []

def getBPM(app, filename):
    return bpm_detection.main(app.filename)

def timerFired(app):
    # newTime = time.time()
    # timePassed = newTime - app.startTime
    app.timerDelay
    app.timeElapsed += app.timerDelay
    createEgg(app)
    moveEgg(app)
    # if (app.timeElapsed // app.timerDelay) % 2 == 0:
    #     addEgg(app)
    # else:
    #     removeEgg(app)
    


runApp(width=1000, height=1000)