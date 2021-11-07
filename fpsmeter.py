import time

class FPSmeter():

    FRAMESINTERVAL = 50

    def __init__(self):
        self.timestamps = []
        self.fps = 0

    def addFrame(self):
        self.timestamps.append(time.perf_counter())
        while len(self.timestamps) > self.FRAMESINTERVAL:
            self.timestamps.pop(0)
        timeInterval = self.timestamps[-1] - self.timestamps[0]
        if (timeInterval > 0):
            self.fps = self.FRAMESINTERVAL / (timeInterval)

    def getFPS(self):
        return self.fps