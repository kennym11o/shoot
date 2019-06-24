import math

class Circle():
    def __init__(self, pos, r, r1, r2, xSpeed = 0, ySpeed = 0, t=3000):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.r = r
        self.r1 = r1
        self.r2 = r2
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.t = t
        self.stop = 0
    def onRange(self, x, y):
        if self.distance(x, y) <= self.r2:
            return 3
        elif self.distance(x, y) <= self.r1:
            return 2
        elif self.distance(x, y) <= self.r:
            return 1
        else:
            return 0
    def distance(self, x, y):
        return math.sqrt((x-self.x)*(x-self.x) + (y-self.y)*(y-self.y))
    def move(self):
        if self.stop == 0:
            self.x += self.xSpeed
            self.y += self.ySpeed
            self.pos = (self.x,self.y)
    def outofscreen(self, w, l):
        if self.x + self.r <=  0 or self.x - self.r >= w or self.y + self.r <= 0 or self.y - self.r >= l:
            return True
        else:
            return False
    def sightOpenMode(self, x, y, magnification):
        self.r*=magnification
        self.r1*=magnification
        self.r2*=magnification
        self.xSpeed*=magnification
        self.ySpeed*=magnification
        self.x = math.floor((self.x - x)*magnification + x)
        self.y = math.floor((self.y - y)*magnification + y)
        self.pos = (self.x, self.y)
    def sightCloseMode(self, x, y, magnification):
        self.r//=magnification
        self.r1//=magnification
        self.r2//=magnification
        self.xSpeed//=magnification
        self.ySpeed//=magnification
        self.x = math.floor((self.x - x)//magnification + x//1)
        self.y = math.floor((self.y - y)//magnification + y//1)
        self.pos = (self.x, self.y)
    def print(self):
        print("x: " + str(self.x) + "\ny:" + str(self.y) + "\nr: " +str(self.r) + "\nr1: " + str(self.r1) + "\nr2: " + str(self.r2))
