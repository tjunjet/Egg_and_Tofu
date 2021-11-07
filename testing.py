from cmu_112_graphics import *
#from
# http://clipart-library.com/free/egg-png-transparent.html
# https://genshin-impact.fandom.com/wiki/Almond_Tofu
def appStarted(app):
    app.image1 = app.loadImage(r"C:\Users\User\Documents\Freshman\15112\Week 10\Egg_and_Tofu\Image\Egg.png")
    app.image2 = app.loadImage(r"C:\Users\User\Documents\Freshman\15112\Week 10\Egg_and_Tofu\Image\Tofu.png")


def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'red')
    #canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.image1))
    canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.image2))

runApp(width=700, height=600)