import pygame as pg
import os
pg.init()


# ----- Sprites --------------------------------------

pg.display.set_mode((800,600))

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

