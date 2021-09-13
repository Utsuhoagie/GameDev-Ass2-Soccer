import pygame as pg
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
BALL_1 = pg.image.load(os.path.join("Sprites\Ball","b1.png"))
BALL_2 = pg.image.load(os.path.join("Sprites\Ball","b2.png"))
BALL_3 = pg.image.load(os.path.join("Sprites\Ball","b3.png"))
BALL_4 = pg.image.load(os.path.join("Sprites\Ball","b4.png"))
BALL_5 = pg.image.load(os.path.join("Sprites\Ball","b5.png"))
BALL_6 = pg.image.load(os.path.join("Sprites\Ball","b6.png"))
BALL_SPRITES = [BALL_1, BALL_2, BALL_3, BALL_4, BALL_5, BALL_6]

# ----- Audio ---------------------------------------

# ----- Gameplay ------------------------------------

# ----- Objects -------------------------------------



# ----- Helper functions -----------------------------------

def addVec(v1: tuple, v2: tuple) -> tuple:
    return (v1[0] + v2[0], v1[1] + v2[1])

def subVec(v1: tuple, v2: tuple) -> tuple:
    return (v1[0] - v2[0], v1[1] - v2[1])

def scalProdVec(x: int, v: tuple) -> tuple:
    return (v[0] * x, v[1] * x)

def dotProdVec(v1: tuple, v2: tuple) -> int:
    return v1[0]*v2[0] + v1[1]*v2[1]

def crossProdVec(v1: tuple, v2: tuple) -> tuple:
    pass

def reflectVec(v1: tuple, n: tuple) -> tuple:
    # note that n is normed <=> n = (1,0) | (-1,0) | ...
    v2 = subVec(v1, scalProdVec(dotProdVec(v1,n)*2, n))
    return v2


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
        self.framesNum = 6
        self.isAnimated = False
        self.image = self.frames[0]           # the rotated image,  it should be reset to orig then rotated, every frame
        self.currentImageIndex = 0
        self.origFrames = self.frames     # DO NOT CHANGE
        self.animationSpeed = 0

        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
        self.moveVector = (2,-2)
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
        self.angle = getAngle(self.moveVector)
        self.image = pg.transform.rotate(self.origFrames[int(self.currentImageIndex)], -self.angle)   # rotate original image only
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if self.isAnimated:
            self.currentImageIndex += self.animationSpeed

            if self.currentImageIndex > self.framesNum - 1:
                self.currentImageIndex = 0
            
            self.image = self.frames[int(self.currentImageIndex)]

        self.move()



class Player(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        

        self.image = pg.Surface((width,height))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.center = [x,y]



class App:
    def __init__(self):
        self.WINDOW_W, self.WINDOW_H = 600,600
        self.screen = pg.display.set_mode((self.WINDOW_W,self.WINDOW_H))
        pg.display.set_caption("Soccer")

        # ----- Gameplay ------------------------------------
        self.FPS = 2

        self.playerSpeed = 5

        # ----- Objects -------------------------------------
        self.field = pg.Rect(20,20,self.WINDOW_W - 40,self.WINDOW_H - 40)

        #self.player = pg.Rect(50,50,40,40)

        # ----- Sprite groups -------------------------------
        self.ball = Ball(150,300)
        self.ballGroup = pg.sprite.Group()

        self.player = Player(200,200,40,40)
        self.playerGroup = pg.sprite.Group()

        self.collideBox = []

    def wallCollision(self) -> tuple:
        """Return tuple of (bool, str)
            where bool = ball is in field
                  str  = which wall it collided"""

        if (self.ball.rect.x > self.field.x and self.ball.rect.x + self.ball.rect.width < self.field.x + self.field.width and
            self.ball.rect.y > self.field.y and self.ball.rect.y + self.ball.rect.height < self.field.y + self.field.height):
            return (False, "")
        elif self.ball.rect.x <= self.field.x:
            return (True, "L")
        elif self.ball.rect.x + self.ball.rect.width >= self.field.x + self.field.width:
            return (True, "R")
        elif self.ball.rect.y <= self.field.y:
            return (True, "U")
        elif self.ball.rect.y + self.ball.rect.height >= self.field.y + self.field.height:
            return (True, "D")

    def playerCollision(self) -> tuple:
        """Return tuple of (bool, str)
            where bool = ball collides
                  str  = which side of player it collided"""
        #if self.ball.rect.colliderect(self.player):
        for collision in pg.sprite.spritecollide(self.ball, self.playerGroup,False):
            # print("abc")
            clipBox = self.ball.rect.clip(collision.rect)
            print("Collision rect: (" + str(clipBox.x) + ", " + str(clipBox.y) + ") | " + str(clipBox.width) + "x" + str(clipBox.height))
            self.collideBox.append(clipBox)
            #pg.draw.rect(self.screen, BROWN, clipBox)
            #pg.display.update()



    def update(self):
        # Player input
        keysPressed = pg.key.get_pressed()

        if keysPressed[pg.K_UP] and self.player.rect.y > self.field.y:
            self.player.rect.y -= self.playerSpeed
        if keysPressed[pg.K_DOWN] and self.player.rect.y + self.player.rect.height < self.field.y + self.field.height:
            self.player.rect.y += self.playerSpeed
        if keysPressed[pg.K_LEFT] and self.player.rect.x > self.field.x:
            self.player.rect.x -= self.playerSpeed
        if keysPressed[pg.K_RIGHT] and self.player.rect.x + self.player.rect.width < self.field.x + self.field.width:
            self.player.rect.x += self.playerSpeed

        #print("Player: " + str(self.player.x) + " " + str(self.player.y))

        # ball natural moving/bouncing
        if self.wallCollision()[0]:
            n = ()
            if self.wallCollision()[1] == "L":
                n = (1,0)
            elif self.wallCollision()[1] == "R":
                n = (-1,0)
            elif self.wallCollision()[1] == "U":
                n = (0,1)
            elif self.wallCollision()[1] == "D":
                n = (0,-1)
            
            self.ball.moveVector = reflectVec(self.ball.moveVector, n)

        # ball colliding with player
        self.playerCollision()



    def draw(self):
        self.screen.fill(BLACK)

        currentSpeed = "(" + str(self.ball.moveVector[0]) + ", " + str(self.ball.moveVector[1]) + ") - (" + str(self.player.rect.x) + ", " + str(self.player.rect.y) + ")"
        speedText = MAIN_FONT.render(currentSpeed,1,WHITE)
        self.screen.blit(speedText,(self.WINDOW_W//2 - speedText.get_width()//2, 7))

        pg.draw.rect(self.screen, GREEN, self.field)

        # pg.draw.rect(self.screen,BROWN,self.ball)
        # radius = self.ball.rect.width // 2
        # pg.draw.circle(self.screen, BROWN, (self.ball.rect.x + radius, self.ball.rect.y + radius), radius)

        # pg.draw.rect(self.screen, RED, self.player)
        self.playerGroup.add(self.player)
        self.playerGroup.update()
        self.playerGroup.draw(self.screen)

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