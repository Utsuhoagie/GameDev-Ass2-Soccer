import pygame as pg
from pygame import *
import os
import random
from math import *
pg.init()

# ----- Window --------------------------------------
WIDTH, HEIGHT = 600,600
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Clicky")

# ----- Colors --------------------------------------

BLACK = (0,0,0)
GRAY = (100,100,100)
WHITE = (255,255,255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (252,227,0)
BROWN = (115,67,38)
LIGHTGREEN = (102,199,28)


# ----- Fonts ---------------------------------------

MAIN_FONT = pg.font.SysFont("arial",12)

# ----- Images --------------------------------------

# BALL_IMG = pg.image.load(os.path.join("Sprites", "ball.png"))
BALL_1 = pg.image.load(os.path.join("Sprites\Ball","b1.png")).convert_alpha()
BALL_2 = pg.image.load(os.path.join("Sprites\Ball","b2.png")).convert_alpha()
BALL_3 = pg.image.load(os.path.join("Sprites\Ball","b3.png")).convert_alpha()
BALL_4 = pg.image.load(os.path.join("Sprites\Ball","b4.png")).convert_alpha()
BALL_5 = pg.image.load(os.path.join("Sprites\Ball","b5.png")).convert_alpha()
BALL_6 = pg.image.load(os.path.join("Sprites\Ball","b6.png")).convert_alpha()
BALL_SPRITES = [BALL_1, BALL_2, BALL_3, BALL_4, BALL_5, BALL_6]


P1_SPRITE = pg.image.load(os.path.join("Sprites\Players","blue.png")).convert_alpha()
P2_SPRITE = pg.image.load(os.path.join("Sprites\Players","red.png")).convert_alpha()
# ----- Audio ---------------------------------------

# ----- Gameplay ------------------------------------

# ----- Objects -------------------------------------



# ----- Helper functions -----------------------------------

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            angle_between((1, 0, 0), (1, 0, 0))
            0.0
            angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = Vector2(v1).normalize()
    v2_u = Vector2(v2).normalize()
    return v1_u.angle_to(v2_u)


def reverseVec(v: tuple):
    return Vector2(-v[0],-v[1])
    #v = (-v[0], -v[1])
    #print(vec)

def addVec(v1: tuple, v2: tuple) -> tuple:
    return Vector2(v1[0] + v2[0], v1[1] + v2[1])

def subVec(v1: tuple, v2: tuple) -> tuple:
    return Vector2(v1[0] - v2[0], v1[1] - v2[1])

def dotProdVec(v1: tuple, v2: tuple) -> int:
    return Vector2(v1[0], v1[1]).dot(v2)

def crossProdVec(v1: tuple, v2: tuple) -> tuple:
    pass

def reflectVec(v1: tuple, n: tuple) -> tuple:
    # note that n is normed <=> n = (1,0) | (-1,0) | ...
    v2 = Vector2(v1).reflect(n)
    return v2

def lengthVec(v: tuple) -> float:
    return Vector2(v).length()

def unitVec(v):
    """ Returns the unit vector of the vector.  """
    resultVec = Vector2(v)
    return resultVec.normalize()

def unitVecKeepSpeed(v: tuple, speed: float) -> tuple:
    if lengthVec(v) != 0:
        return (v[0]*speed/lengthVec(v), v[1]*speed/lengthVec(v))
    else:
        return (v[0]*speed/(lengthVec(v)+0.1), v[1]*speed/(lengthVec(v)+0.1))

def getAngle(vec: tuple) -> float:
    arccos = float(vec[0]/sqrt(pow(vec[0],2) + pow(vec[1],2)))
    angle = degrees(acos(arccos))
    if vec[1] < 0:
        angle *= -1
    return angle


# ----- Classes -------------------------------------

class Ball(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.frames = BALL_SPRITES
        self.maxFrames = 6

        

        self.isAnimated = False
        self.image = self.frames[0]             # the rotated image,  it should be reset to orig then rotated, every frame
        self.currentImageIndex = 0
        self.origFrames = self.frames           # DO NOT CHANGE
        self.animationSpeed = 0

        # for accurate collision with players
        self.mask = pg.mask.from_surface(self.image)
        
        # for easy collision with walls
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
        #self.moveVector = (0.3999999999999999, -2.7999999999999994)
        self.moveVector = Vector2(2,2)
        self.moveVectorTimesChanged = 0         # check if it is stuck
        self.wallStuck = ""                     # which wall the ball is stuck in
        self.angle = 0.0

    def move(self):
        self.isAnimated = True
        self.animationSpeed = (pow(self.moveVector[0],2) + pow(self.moveVector[1],2) + 10)/120
            # don't pay attention to the numbers, this just looks nice

        self.rect.x += self.moveVector[0]
        self.rect.y += self.moveVector[1]
        self.rotate()   # rotate ball so it rolls forward

    def rotate(self):
        """rotate an image while keeping its center"""
        #self.angle = getAngle(self.moveVector)
        self.angle = self.moveVector.angle_to(Vector2(1,0))
        self.image = pg.transform.rotate(self.origFrames[int(self.currentImageIndex)], -self.angle)   # rotate original image only
        self.rect = self.image.get_rect(center=self.rect.center)

    def fixBallPos(self, displace: int):
        # displace for player collision should be bigger than displace for wall collision

        if self.wallStuck == "L":
            self.rect.x += displace
        if self.wallStuck == "R":
            self.rect.x -= displace
        if self.wallStuck == "U":
            self.rect.y += displace
        if self.wallStuck == "D":
            self.rect.y -= displace

    def update(self):
        if self.moveVectorTimesChanged > 0:
            if self.moveVectorTimesChanged >= 10:
                self.fixBallPos(5)    # fix the ball position
                self.moveVectorTimesChanged -= 4
                if self.moveVectorTimesChanged < 0:
                    self.moveVectorTimesChanged = 0
            else:
                self.moveVectorTimesChanged -= 1
        
        if self.moveVector.length() == 0:
            self.isAnimated = False

        if self.isAnimated:
            self.currentImageIndex += self.animationSpeed

            if self.currentImageIndex > self.maxFrames - 1:
                self.currentImageIndex = 0
            
            self.image = self.frames[int(self.currentImageIndex)]
            self.mask = pg.mask.from_surface(self.image)

        self.move()



class Player(pg.sprite.Sprite):
    def __init__(self, x, y, pImage):
        super().__init__()

        self.frames = [pImage]
        self.maxFrames = 1

        self.isAnimated = False
        self.image = self.frames[0]
        self.currentImageIndex = 0
        self.origFrames = self.frames           # DO NOT CHANGE
        self.animationSpeed = 0
        self.facing = {"left": 0, "right": 0, "up": 0, "down": 0}

        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

        self.wallStuck = ""
        self.speed = 4

        # for accurate collision with ball
        self.mask = pg.mask.from_surface(self.image)
        
        # for easy collision with walls
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
        self.angle = 0.0

    def getStringFromFace(self) -> str:
        result = ""
        for face in self.facing:
            result += str(self.facing[face])

        return result

    def rotate(self):
        """rotate an image while keeping its center"""
        currentFace = self.getStringFromFace()

        if currentFace in ["1000", "1011"]:
            # face left, move left
            if "L" not in self.wallStuck:
                self.rect.x -= self.speed
            self.angle = 180
        elif currentFace in ["0100", "0111"]:
            # face right, move right
            if "R" not in self.wallStuck:
                self.rect.x += self.speed
            self.angle = 0
        elif currentFace in ["0010", "1110"]:
            # face up, move up
            if "U" not in self.wallStuck:
                self.rect.y -= self.speed
            self.angle = 90
        elif currentFace in ["0001", "1101"]:
            # face down, move down
            if "D" not in self.wallStuck:
                self.rect.y += self.speed
            self.angle = -90
        elif currentFace == "1010":
            # face up left
            if ("L" not in self.wallStuck) and ("U" not in self.wallStuck):
                self.rect.x -= self.speed
                self.rect.y -= self.speed
            elif "L" not in self.wallStuck:
                self.rect.x -= self.speed
            elif "U" not in self.wallStuck:
                self.rect.y -= self.speed
            self.angle = 135
        elif currentFace == "0101":
            # face down right
            if ("R" not in self.wallStuck) and ("D" not in self.wallStuck):
                self.rect.x += self.speed
                self.rect.y += self.speed
            elif "R" not in self.wallStuck:
                self.rect.x += self.speed
            elif "D" not in self.wallStuck:
                self.rect.y += self.speed
            self.angle = -45
        elif currentFace == "1001":
            # face down left
            if ("L" not in self.wallStuck) and ("D" not in self.wallStuck):
                self.rect.x -= self.speed
                self.rect.y += self.speed
            elif "L" not in self.wallStuck:
                self.rect.x -= self.speed
            elif "D" not in self.wallStuck:
                self.rect.y += self.speed
            self.angle = -135
        elif currentFace == "0110":
            # face up right
            if ("R" not in self.wallStuck) and ("U" not in self.wallStuck):
                self.rect.x += self.speed
                self.rect.y -= self.speed
            elif "R" not in self.wallStuck:
                self.rect.x += self.speed
            elif "U" not in self.wallStuck:
                self.rect.y -= self.speed
            self.angle = 45
        
            
        # self.angle = getAngle(self.moveVector)
        self.image = pg.transform.rotate(self.origFrames[int(0)], self.angle)   # rotate original image only
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rotate()

        self.wallStuck = ""

        self.facing = self.facing.fromkeys(self.facing,0)



class App:
    def __init__(self):
        self.WINDOW_W, self.WINDOW_H = 600,600
        self.screen = pg.display.set_mode((self.WINDOW_W,self.WINDOW_H))
        pg.display.set_caption("Soccer")

        # ----- Gameplay ------------------------------------
        self.FPS = 60

        self.playerSpeed = 5

        # ----- Objects -------------------------------------
        self.field = pg.Rect(20,20,self.WINDOW_W - 40,self.WINDOW_H - 40)
        self.fieldBuffer = 0
        #self.player = pg.Rect(50,50,40,40)

        # ----- Sprite groups -------------------------------
        self.ball = Ball(50,50)
        self.ballGroup = pg.sprite.Group()

        self.p1 = Player(200,250, P1_SPRITE)
        self.p2 = Player(400,450, P2_SPRITE)
        self.playerGroup = pg.sprite.Group()
        

        self.collideBox = []

    def wallCollision(self) -> tuple:
        """Return tuple of (bool, str)
            where bool = ball is in field
                  str  = which wall it collided"""
        ballRX, ballRY, ballRW, ballRH = int(self.ball.rect.x), int(self.ball.rect.y), int(self.ball.rect.width), int(self.ball.rect.height)
        fieldX, fieldY, fieldW, fieldH = int(self.field.x), int(self.field.y), int(self.field.width), int(self.field.height)

        if (ballRX > fieldX and ballRX + ballRW < fieldX + fieldW + self.fieldBuffer and
            ballRY > fieldY and ballRY + ballRH < fieldY + fieldH - self.fieldBuffer):
            return (False, "")
        elif ballRX <= fieldX:
            self.ball.moveVectorTimesChanged +=1
            self.ball.wallStuck = "L"
            return (True, "L")
        elif ballRX + ballRW >= fieldX + fieldW: # + self.fieldBuffer:
            self.ball.moveVectorTimesChanged +=1
            self.ball.wallStuck = "R"
            return (True, "R")
        elif ballRY <= fieldY + self.fieldBuffer:
            self.ball.moveVectorTimesChanged +=1
            self.ball.wallStuck = "U"
            return (True, "U")
        elif ballRY + ballRH >= fieldY + fieldH - self.fieldBuffer:
            self.ball.moveVectorTimesChanged +=1
            self.ball.wallStuck = "D"
            return (True, "D")

        # if (self.ball.rect.x > self.field.x and self.ball.rect.x + self.ball.rect.width < self.field.x + self.field.width + self.fieldBuffer and
        #     self.ball.rect.y > self.field.y and self.ball.rect.y + self.ball.rect.height < self.field.y + self.field.height - self.fieldBuffer):
        #     return (False, "")
        # elif self.ball.rect.x <= self.field.x:
        #     return (True, "L")
        # elif self.ball.rect.x + self.ball.rect.width >= self.field.x + self.field.width:
        #     return (True, "R")
        # elif self.ball.rect.y <= self.field.y:
        #     return (True, "U")
        # elif self.ball.rect.y + self.ball.rect.height >= self.field.y + self.field.height:
        #     return (True, "D")


    def playerCollision(self) -> tuple:
        """Return tuple of (bool, str)
            where bool = ball collides
                  str  = which side of player it collided"""
        #if self.ball.rect.colliderect(self.player):
        for collision in pg.sprite.spritecollide(self.ball, self.playerGroup, False, pg.sprite.collide_mask):
            # clipBox = self.ball.rect.clip(collision.rect)
            # print("Collision rect: (" + str(clipBox.x) + ", " + str(clipBox.y) + ") | " + str(clipBox.width) + "x" + str(clipBox.height))
            # self.collideBox.append(clipBox)


            offset = (self.ball.rect.center[0] - collision.rect.center[0], self.ball.rect.center[1] - collision.rect.center[1])
            collisionPoint = self.ball.mask.overlap(collision.mask, offset)

            if collisionPoint is not None:


                print("Collides at " + str(collisionPoint))
                relativeCenter = (self.p1.rect.center[0] - self.p1.rect.x, self.p1.rect.center[1] - self.p1.rect.y)
                print("Relative center is " + str(relativeCenter))

                leftSide = ((0,0), (self.p1.rect.width//2, self.p1.rect.height))
                rightSide = ((self.p1.rect.width//2,0),(self.p1.rect.width,self.p1.rect.height))
                topSide = ((0,0), (self.p1.rect.width, self.p1.rect.height//2))
                bottomSide = ((0,self.p1.rect.height//2),(self.p1.rect.width,self.p1.rect.height))

                reflectVec = unitVecKeepSpeed((collisionPoint[0] - relativeCenter[0], collisionPoint[1] - relativeCenter[1]), lengthVec(self.ball.moveVector))
                print("Reflection vector is " + str(reflectVec))
                
                if collisionPoint in leftSide:
                    self.ball.wallStuck = "R"
                    self.ball.fixBallPos(15)
                if collisionPoint in rightSide:
                    self.ball.wallStuck = "L"
                    self.ball.fixBallPos(15)
                if collisionPoint in topSide:
                    self.ball.wallStuck = "D"
                    self.ball.fixBallPos(15)
                if collisionPoint in bottomSide:
                    self.ball.wallStuck = "U"
                    self.ball.fixBallPos(15)

                self.ball.moveVector = Vector2(reflectVec)
                # self.ball.moveVectorTimesChanged += 1
                # this should bounce the ball back, using new vector



    def update(self):

        # P1 input
        keysPressed = pg.key.get_pressed()

        if keysPressed[pg.K_UP]:
            if self.p1.rect.y <= self.field.y:
                self.p1.wallStuck += "U"
            #self.p1.rect.y -= self.playerSpeed
            self.p1.facing["up"] = 1
        if keysPressed[pg.K_DOWN]:
            if self.p1.rect.y + self.p1.rect.height >= self.field.y + self.field.height:
                self.p1.wallStuck += "D"
            #self.p1.rect.y += self.playerSpeed
            self.p1.facing["down"] = 1
        if keysPressed[pg.K_LEFT]:
            if self.p1.rect.x <= self.field.x:
                self.p1.wallStuck += "L"
            #self.p1.rect.x -= self.playerSpeed
            self.p1.facing["left"] = 1
        if keysPressed[pg.K_RIGHT]:
            if self.p1.rect.x + self.p1.rect.width >= self.field.x + self.field.width:
                self.p1.wallStuck += "R"
            #self.p1.rect.x += self.playerSpeed
            self.p1.facing["right"] = 1

        if keysPressed[pg.K_w]:
            if self.p2.rect.y <= self.field.y:
                self.p2.wallStuck += "U"
            #self.p2.rect.y -= self.playerSpeed
            self.p2.facing["up"] = 1
        if keysPressed[pg.K_s]:
            if self.p2.rect.y + self.p2.rect.height >= self.field.y + self.field.height:
                self.p2.wallStuck += "D"
            #self.p2.rect.y += self.playerSpeed
            self.p2.facing["down"] = 1
        if keysPressed[pg.K_a]:
            if self.p2.rect.x <= self.field.x:
                self.p2.wallStuck += "L"
            #self.p2.rect.x -= self.playerSpeed
            self.p2.facing["left"] = 1
        if keysPressed[pg.K_d]:
            if self.p2.rect.x + self.p2.rect.width >= self.field.x + self.field.width:
                self.p2.wallStuck += "R"
            #self.p2.rect.x += self.playerSpeed
            self.p2.facing["right"] = 1

        #print("Player: " + str(self.p1.x) + " " + str(self.p1.y))

        # ball natural bouncing with walls
        if not self.wallCollision()[0]:
            pass
        elif self.wallCollision()[0]:
            n = ()
            if self.wallCollision()[1] == "L":
                n = (1,0)
            elif self.wallCollision()[1] == "R":
                n = (-1,0)
            elif self.wallCollision()[1] == "U":
                n = (0,1)
            elif self.wallCollision()[1] == "D":
                n = (0,-1)
            
            self.ball.moveVector = Vector2(reflectVec(self.ball.moveVector, n))

        # ball colliding with player
        self.playerCollision()



    def draw(self):
        self.screen.fill(BLACK)


        currentSpeed = "(" + str(self.ball.moveVector[0]) + ", " + str(self.ball.moveVector[1]) + ") - (" + str(self.p1.rect.center[0]) + ", " + str(self.p1.rect.center[1]) + ")"
        speedText = MAIN_FONT.render(currentSpeed,1,WHITE)
        self.screen.blit(speedText,(self.WINDOW_W//2 - speedText.get_width()//2, 7))

        # print times moveVector changed
        # print(self.ball.moveVectorTimesChanged)

        pg.draw.rect(self.screen, GREEN, self.field)

        # pg.draw.rect(self.screen,BROWN,self.ball)
        # radius = self.ball.rect.width // 2
        # pg.draw.circle(self.screen, BROWN, (self.ball.rect.x + radius, self.ball.rect.y + radius), radius)

        # pg.draw.rect(self.screen, RED, self.player)
        self.playerGroup.add(self.p1)
        self.playerGroup.add(self.p2)
        self.playerGroup.update()
        self.playerGroup.draw(self.screen)


        """Draw mask, for testing"""
        # otuple = self.ball.mask.outline()
        # olist = list()
        # for point in otuple:
        #     listPoint = [point[0] + 50, point[1] + 50]
        #     olist.append(listPoint)
        #     # point[0] += 50
        #     # point[1] += 50
        #     # print(type(point))
        # pg.draw.polygon(self.screen,(WHITE),olist)


        # Ball sprite!!!!
        # print("Ball pos: " + str(self.ball.rect.x) + " " + str(self.ball.rect.y))
        self.ballGroup.add(self.ball)
        self.ballGroup.update()
        self.ballGroup.draw(self.screen)

        for collideBox in self.collideBox:
            pg.draw.rect(self.screen, BROWN, collideBox)

        self.collideBox.clear()


        pg.display.update()

    def run(self):
        runFlag = True
        clock = pg.time.Clock()

        while runFlag:
            clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runFlag = False
                    break

            self.update()

            self.draw()

        pg.quit()


# ---------- Handlers -------------

# ---------- Draw -----------------

# ----- Main ----------------------------------------


if __name__ == '__main__':
    App().run()