# Create multiple classes for the different objects.
import random
from intersection import *

class Egg(object):
    # Egg object takes in a filename
    # Attribute to the egg's weight
    def __init__(self, filename):
        self.filename = filename
        self.points = 10
        #checks if it is sliced
        self.slice = False
        self.x = random.randint(100, 900)
        self.y = 0
        self.boxRadius = 100

    # Check if egg is sliced
    #x0 and y0 are classes of points on the point class from opencv
    def sliced(self, x0, y0): 
        #top left corner
        top_left = Point(self.x - self.boxRadius, self.y- self.boxRadius)
        #top right corner
        top_right = Point(self.x + self.boxRadius, self.y - self.boxRadius)
        #bot left
        bot_left = Point(self.x - self.boxRadius, self.y + self.boxRadius)
        #bot_right
        bot_right = Point(self.x + self.boxRadius, self.y + self.boxRadius)
        if doIntersect(top_left, top_right, x0, y0):
            self.slice = True
        if doIntersect(top_left, bot_left, x0, y0):
            self.slice =  True
        if doIntersect(top_right, bot_right, x0, y0):
            self.slice = True
        if doIntersect(bot_left, bot_right, x0, y0):
            self.slice = True    


class RedEgg(Egg):
    def __init__(self, filename):
        super().__init__(filename)
        self.weight = 10
        self.droptime = 0
        self.speed = 0

class BlueEgg(Egg):
    def __init__(self, filename):
        super().__init__(filename)
        self.weight = 20
        self.droptime = 0
        self.speed = 0

class GreenEgg(Egg):
    def __init__(self, filename):
        super().__init__(filename)
        self.weight = 30
        self.droptime = 0
        self.speed = 0

class Tofu(object):
    def __init__(self, filename):
        self.filename = filename
        self.points = 20
        self.slice = False
        self.x = random.randint(100, 900)
        self.y = 0
        self.boxRadius = 100

    def sliced(self, x0, y0): 
        #top left corner
        top_left = Point(self.x - self.boxRadius, self.y- self.boxRadius)
        #top right corner
        top_right = Point(self.x + self.boxRadius, self.y - self.boxRadius)
        #bot left
        bot_left = Point(self.x - self.boxRadius, self.y + self.boxRadius)
        #bot_right
        bot_right = Point(self.x + self.boxRadius, self.y + self.boxRadius)
        if doIntersect(top_left, top_right, x0, y0):
            self.slice = True
        if doIntersect(top_left, bot_left, x0, y0):
            self.slice =  True
        if doIntersect(top_right, bot_right, x0, y0):
            self.slice = True
        if doIntersect(bot_left, bot_right, x0, y0):
            self.slice = True 
    