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
        
        #self.moveVector = (0.3999999999999999, -2.7999999999999994)
        self.moveVector = Vector2(3.5,1)
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
        if self.moveVectorTimesChanged > 0:
            if self.moveVectorTimesChanged >= 20:
                self.fixBallPos(25)
                self.moveVectorTimesChanged -= 10
                if self.moveVectorTimesChanged < 0:
                    self.moveVectorTimesChanged = 0
            elif self.moveVectorTimesChanged >= 10:
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
