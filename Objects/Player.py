import pygame as pg
pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, pImage: pg.Surface, ID: int):
        super().__init__()
        self.ID = ID

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
        self.speed = 5
        self.origSpeed = self.speed

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
        
        # try to reset speed
        # if no collision, this will stay as normal
        self.speed = self.origSpeed

        # self.angle = getAngle(self.moveVector)
        self.image = pg.transform.rotate(self.origFrames[int(0)], self.angle)   # rotate original image only
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rotate()

        self.wallStuck = ""

        self.facing = self.facing.fromkeys(self.facing,0)
