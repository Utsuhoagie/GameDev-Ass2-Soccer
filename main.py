import pygame as pg
from pygame import *
import os
import random
from math import *
from Helper import *

from Objects.Player import *
from Objects.Ball import *
from Objects.Assets import *

pg.init()

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

# ----- Classes -------------------------------------

class App:
    def __init__(self):
        self.WINDOW_W, self.WINDOW_H = 800, 600
        self.screen = pg.display.set_mode((self.WINDOW_W,self.WINDOW_H))
        pg.display.set_caption("Soccer")

        # ----- Gameplay ------------------------------------
        self.FPS = 60

        self.playerSpeed = 5

        # ----- Objects -------------------------------------
        self.field = pg.Rect(20,20,self.WINDOW_W - 40,self.WINDOW_H - 40)
        self.fieldBuffer = 0

        # ----- Sprite groups -------------------------------
        self.ball = Ball(50,50)
        self.ballGroup = pg.sprite.Group()

        self.p1 = Player(200,250, P1_SPRITE, 1)
        self.p2 = Player(400,450, P2_SPRITE, 2)
        self.playerGroup = pg.sprite.Group()

    def wallBounce(self):
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
            
            self.ball.moveVector = Vector2(self.ball.moveVector.reflect(n))

    def wallCollision(self) -> tuple:
        """Return tuple of (bool, str)
            where bool = ball is in field
                  str  = which wall it collided"""
        ballRX, ballRY, ballRW, ballRH = (
            int(self.ball.rect.x), int(self.ball.rect.y), int(self.ball.rect.width), int(self.ball.rect.height))
        fieldX, fieldY, fieldW, fieldH = (
            int(self.field.x), int(self.field.y), int(self.field.width), int(self.field.height))

        if (ballRX > fieldX and ballRX + ballRW < fieldX + fieldW and
            ballRY > fieldY and ballRY + ballRH < fieldY + fieldH):
            return (False, "")
        elif ballRX <= fieldX:
            self.ball.moveVectorTimesChanged +=1
            self.ball.wallStuck = "L"
            return (True, "L")
        elif ballRX + ballRW >= fieldX + fieldW:
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


    def playerCollision(self) -> tuple:
        """Return tuple of (bool, str)
            where bool = ball collides
                  str  = which side of player it collided"""
        #if self.ball.rect.colliderect(self.player):
        for playerCollide in pg.sprite.spritecollide(self.ball, self.playerGroup, False, pg.sprite.collide_mask):
            offset = (self.ball.rect.center[0] - playerCollide.rect.center[0], self.ball.rect.center[1] - playerCollide.rect.center[1])
            collisionPoint = self.ball.mask.overlap(playerCollide.mask, offset)

            if collisionPoint is not None:
                # print("Collides at " + str(collisionPoint))
                relativeCenter = Vector2(self.p1.rect.center[0] - self.p1.rect.x, self.p1.rect.center[1] - self.p1.rect.y)
                # print("Relative center is " + str(relativeCenter))

                leftSide = ((0,0), (playerCollide.rect.width//2, playerCollide.rect.height))
                rightSide = ((playerCollide.rect.width//2,0), (playerCollide.rect.width, playerCollide.rect.height))
                topSide = ((0,0), (playerCollide.rect.width, playerCollide.rect.height//2))
                bottomSide = ((0, playerCollide.rect.height//2), (playerCollide.rect.width, playerCollide.rect.height))

                reflectVec = unitVecKeepSpeed(Vector2(collisionPoint[0] - relativeCenter[0], collisionPoint[1] - relativeCenter[1]), self.ball.moveVector.length())
                # reflectVec = self.ball.moveVector.reflect((relativeCenter[0] - collisionPoint[0], relativeCenter[1] - collisionPoint[1]))
                # print("Reflection vector is " + str(reflectVec))
                
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

                #self.ball.moveVector = Vector2(reflectVec)
                self.ball.moveVector = reflectVec

                # slow player down, until no more collision
                playerCollide.speed = 1


    def handleInput(self, player: Player):
        # P1 input
        keysPressed = pg.key.get_pressed()

        if player.ID == 1:
            if keysPressed[pg.K_UP]:
                if self.p1.rect.y <= self.field.y:
                    self.p1.wallStuck += "U"
                self.p1.facing["up"] = 1
            if keysPressed[pg.K_DOWN]:
                if self.p1.rect.y + self.p1.rect.height >= self.field.y + self.field.height:
                    self.p1.wallStuck += "D"
                self.p1.facing["down"] = 1
            if keysPressed[pg.K_LEFT]:
                if self.p1.rect.x <= self.field.x:
                    self.p1.wallStuck += "L"
                self.p1.facing["left"] = 1
            if keysPressed[pg.K_RIGHT]:
                if self.p1.rect.x + self.p1.rect.width >= self.field.x + self.field.width:
                    self.p1.wallStuck += "R"
                self.p1.facing["right"] = 1

        elif player.ID == 2:
            # P2 input
            if keysPressed[pg.K_w]:
                if self.p2.rect.y <= self.field.y:
                    self.p2.wallStuck += "U"
                self.p2.facing["up"] = 1
            if keysPressed[pg.K_s]:
                if self.p2.rect.y + self.p2.rect.height >= self.field.y + self.field.height:
                    self.p2.wallStuck += "D"
                self.p2.facing["down"] = 1
            if keysPressed[pg.K_a]:
                if self.p2.rect.x <= self.field.x:
                    self.p2.wallStuck += "L"
                self.p2.facing["left"] = 1
            if keysPressed[pg.K_d]:
                if self.p2.rect.x + self.p2.rect.width >= self.field.x + self.field.width:
                    self.p2.wallStuck += "R"
                self.p2.facing["right"] = 1

    def update(self):

        # Player inputs
        self.handleInput(self.p1)
        self.handleInput(self.p2)

        # Ball natural bouncing with walls
        self.wallBounce()

        # ball colliding with player
        self.playerCollision()


    def draw(self):
        self.screen.fill(BLACK)

        currentSpeed = "(" + str(self.ball.moveVector[0]) + ", " + str(self.ball.moveVector[1]) + ") - (" + str(self.p1.rect.center[0]) + ", " + str(self.p1.rect.center[1]) + ")"
        speedText = MAIN_FONT.render(currentSpeed,1,WHITE)
        self.screen.blit(speedText,(self.WINDOW_W//2 - speedText.get_width()//2, 7))

        pg.draw.rect(self.screen, GREEN, self.field)

        self.playerGroup.add(self.p1)
        self.playerGroup.add(self.p2)
        self.playerGroup.update()

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

        self.ballGroup.add(self.ball)
        self.ballGroup.update()

        self.ballGroup.draw(self.screen)
        self.playerGroup.draw(self.screen)

        pg.display.update()

    def run(self):
        runFlag = True
        clock = pg.time.Clock()

        while runFlag:
            clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
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