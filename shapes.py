# Create multiple classes for the different objects.
import random
from intersection import *

class Egg(object):
    # Egg object takes in a filename
    # Attribute to the egg's weight
    def __init__(self, filename, width, height):
        self.filename = filename
        self.width = width
        self.height = height
        self.points = 10
        #checks if it is sliced
        self.slice = False
        self.x = random.randint(100, 900)
        self.y = 0
        self.boxRadiusWidth = self.width//2
        self.boxRadiusLength = self.height//2
        self.counter = 0

    # Check if egg is sliced
    #x0 and y0 are classes of points on the point class from opencv
    def sliced(self, x0, y0): 
        #top left corner
        top_left = Point(self.x - self.boxRadiusWidth, self.y - self.boxRadiusLength)
        #top right corner
        top_right = Point(self.x + self.boxRadiusWidth, self.y - self.boxRadiusLength)
        #bot left
        bot_left = Point(self.x - self.boxRadiusWidth, self.y + self.boxRadiusLength)
        #bot_right
        bot_right = Point(self.x + self.boxRadiusWidth, self.y + self.boxRadiusLength)
        if doIntersect(top_left, top_right, x0, y0):
            self.slice = True
        if doIntersect(top_left, bot_left, x0, y0):
            self.slice = True
        if doIntersect(top_right, bot_right, x0, y0):
            self.slice = True
        if doIntersect(bot_left, bot_right, x0, y0):
            self.slice = True

class Tofu(object):
    def __init__(self, filename, width, height):
        self.filename = filename
        self.width = width
        self.height = height
        self.points = 50
        self.slice = False
        self.x = random.randint(100, 900)
        self.y = 0
        self.boxRadiusWidth = self.width//2
        self.boxRadiusLength = self.height//2
        self.counter = 0

    def sliced(self, x0, y0): 
        #top left corner
        top_left = Point(self.x - self.boxRadiusWidth, self.y- self.boxRadiusLength)
        #top right corner
        top_right = Point(self.x + self.boxRadiusWidth, self.y - self.boxRadiusLength)
        #bot left
        bot_left = Point(self.x - self.boxRadiusWidth, self.y + self.boxRadiusLength)
        #bot_right
        bot_right = Point(self.x + self.boxRadiusWidth, self.y + self.boxRadiusLength)
        if doIntersect(top_left, top_right, x0, y0):
            self.slice = True
        if doIntersect(top_left, bot_left, x0, y0):
            self.slice =  True
        if doIntersect(top_right, bot_right, x0, y0):
            self.slice = True
        if doIntersect(bot_left, bot_right, x0, y0):
            self.slice = True    
