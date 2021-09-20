import pygame as pg
import os
from pygame import *
from Objects.Assets import *

class Ball(pg.sprite.Sprite):
    def __init__(self, x, y):
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
        
        #self.mv = (0.3999999999999999, -2.7999999999999994)
        self.mv = Vector2(4,0)
        self.mvTimesChanged = 0         # check if it is stuck
        self.wallStuck = ""                     # which wall the ball is stuck in
        self.angle = 0.0

        self.frictionTimer = 240

    def move(self):
        


        if abs(self.mv[0]) + abs(self.mv[1]) > 1.5:
            self.isAnimated = True
            self.animationSpeed = (pow(self.mv[0],2) + pow(self.mv[1],2) + 10)/120
                # don't pay attention to the numbers, this just looks nice
        else:
            self.isAnimated = False
            self.mv = Vector2(0,0)
            self.animationSpeed = 0
            self.image = self.frames[int(self.currentImageIndex)]



        self.rect.x += float(self.mv[0])
        self.rect.y += float(self.mv[1])
        
        if self.frictionTimer % 30 == 0 and self.frictionTimer > 0:
            self.mv[0] *= 1
            self.mv[1] *= 1


        self.rotate()   # rotate ball so it rolls forward

    def rotate(self):
        """rotate an image while keeping its center"""
        #self.angle = getAngle(self.mv)
        self.angle = self.mv.angle_to(Vector2(1,0))
        self.image = pg.transform.rotate(self.origFrames[int(self.currentImageIndex)], self.angle)   # rotate original image only
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
        if self.mvTimesChanged > 0:
            # if self.mvTimesChanged >= 20:
            #     self.fixBallPos(25)
            #     self.mvTimesChanged -= 10
            #     if self.mvTimesChanged < 0:
            #         self.mvTimesChanged = 0
            # elif self.mvTimesChanged >= 2:
            if self.mvTimesChanged >= 2:
                self.fixBallPos(5)    # fix the ball position
                self.mvTimesChanged -= 4
                if self.mvTimesChanged < 0:
                    self.mvTimesChanged = 0
            else:
                self.mvTimesChanged -= 1
        
        if self.mv.length() == 0:
            self.isAnimated = False

        if self.isAnimated:
            self.currentImageIndex += self.animationSpeed

            if self.currentImageIndex > self.maxFrames - 1:
                self.currentImageIndex = 0
            
            self.image = self.frames[int(self.currentImageIndex)]
            self.mask = pg.mask.from_surface(self.image)

        if self.frictionTimer > 0:
            self.frictionTimer -= 1

        self.move()
