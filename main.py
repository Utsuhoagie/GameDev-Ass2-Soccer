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

BALL_IMG = pg.image.load(os.path.join("Sprites", "ball.png"))

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
        # self.image = pg.Surface([width, height])
        # self.image.fill(color)
        self.image = BALL_IMG
        self.origImage = self.image
        # self.screen = screen
        # self.image = pg.draw.circle(self.screen, color, (x + width//2, y + height//2), width//2)


        # # pg.draw.rect(self.screen,BROWN,self.ball)
        # # radius = self.ball.rect.width // 2
        # # pg.draw.circle(self.screen, BROWN, (self.ball.rect.x + radius, self.ball.rect.y + radius), radius)

        self.moveVector = (-4,4)

        self.rect = self.image.get_rect()
        self.origRect = self.rect
        # self.rect = self.image
        self.rect.center = [x,y]
        self.origRect.center = self.rect.center

        self.angle = 0.0

    def move(self):
        self.rect.x += self.moveVector[0]
        self.rect.y += self.moveVector[1]
        currentPos = (str(self.rect.x) + ", " + str(self.rect.y))
        self.angle = getAngle(self.moveVector)
        print(currentPos + " and move = " + str(self.moveVector[0]) + ", " + str(self.moveVector[1]))
        # print(self.angle)
        self.rot_center()

    def update(self):
        # self.image = pg.transform.rotate(self.image, self.angle)
        # self.rot_center()
        pass

    def rot_center(self):
        """rotate an image while keeping its center"""
        self.image = pg.transform.rotate(self.origImage, self.angle)
        self.rect = self.image.get_rect(center=self.origRect.center)
        # return rotatedImage, rotatedRect



class App:
    def __init__(self):
        self.WINDOW_W, self.WINDOW_H = 600,600
        self.screen = pg.display.set_mode((self.WINDOW_W,self.WINDOW_H))
        pg.display.set_caption("Test Reflect")

        # ----- Gameplay ------------------------------------
        self.FPS = 60


        self.playerSpeed = 5

        # ----- Objects -------------------------------------
        self.field = pg.Rect(20,20,560,560)

        # self.ball = pg.Rect(150,150,20,20)

        self.player = pg.Rect(300,300,40,40)

        # ----- Sprite groups -------------------------------
        self.ball = Ball(150,150)
        self.ballGroup = pg.sprite.Group()
        # self.ballGroup.add(self.ball)

    def wallCollision(self) -> tuple:
        """Return tuple of (bool, str)
            where bool = ball is in field
                  str  = which wall it collided"""

        if (self.ball.rect.x > self.field.x and self.ball.rect.x + self.ball.rect.width < self.field.x + self.field.width and
            self.ball.rect.y > self.field.y and self.ball.rect.y + self.ball.rect.height < self.field.y + self.field.height):
            return (True, "")
        elif self.ball.rect.x <= self.field.x:
            return (False, "L")
        elif self.ball.rect.x + self.ball.rect.width >= self.field.x + self.field.width:
            return (False, "R")
        elif self.ball.rect.y <= self.field.y:
            return (False, "U")
        elif self.ball.rect.y + self.ball.rect.height >= self.field.y + self.field.height:
            return (False, "D")

    def playerCollision(self) -> tuple:
        """Return tuple of (bool, str)
            where bool = ball collides
                  str  = which side of player it collided"""
        if self.ball.rect.colliderect(self.player):
            # print("abc")
            pass



    def update(self):
        # Player input
        keysPressed = pg.key.get_pressed()

        if keysPressed[pg.K_UP] and self.player.y > self.field.y:
            self.player.y -= self.playerSpeed
        if keysPressed[pg.K_DOWN] and self.player.y + self.player.height < self.field.y + self.field.height:
            self.player.y += self.playerSpeed
        if keysPressed[pg.K_LEFT] and self.player.x > self.field.x:
            self.player.x -= self.playerSpeed
        if keysPressed[pg.K_RIGHT] and self.player.x + self.player.width < self.field.x + self.field.width:
            self.player.x += self.playerSpeed



        # ball colliding with player
        # self.playerCollision()

        # ball natural moving/bouncing
        if self.wallCollision()[0]:
            self.ball.move()
        else:
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
            self.ball.move()

    def draw(self):
        self.screen.fill(BLACK)

        currentSpeed = "(" + str(self.ball.moveVector[0]) + ", " + str(self.ball.moveVector[1]) + ")"
        speedText = MAIN_FONT.render(currentSpeed,1,WHITE)
        self.screen.blit(speedText,(self.WINDOW_W//2 - speedText.get_width()//2, 7))

        pg.draw.rect(self.screen, GREEN, self.field)

        # pg.draw.rect(self.screen,BROWN,self.ball)
        # radius = self.ball.rect.width // 2
        # pg.draw.circle(self.screen, BROWN, (self.ball.rect.x + radius, self.ball.rect.y + radius), radius)

        # Ball sprite!!!!
        self.ballGroup.add(self.ball)
        self.ballGroup.update()
        self.ballGroup.draw(self.screen)

        pg.draw.rect(self.screen, RED, self.player)

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

            keysPressed = pg.key.get_pressed()


            self.update()

            self.draw()

        pg.quit()


# ---------- Handlers -------------

# ---------- Draw -----------------

# ----- Main ----------------------------------------


if __name__ == '__main__':
    App().run()