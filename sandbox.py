import math
import numpy as np

from pygame import *
from typing import *

def foo(x: List[int]) -> int:
    return x[0] * x[0]

print(foo([5]))


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

# def unitVecKeepSpeed(v: tuple, speed: float) -> tuple:
#     unitVec = [v[0]*speed/lengthVec(v), v[1]*speed/lengthVec(v)]
#     # unitVec[0] *= speed
#     # unitVec[1] *= speed
#     return tuple(unitVec)

vec = (2,2)
n = (0,-1)
# vec2 = (3,1)
# print(reflectVec(vec,n))
reverseVec(vec)


# print(str(abs(-5)))



# angleVec = (4,4)
# arccos = float(angleVec[0]/pygame.math.sqrt(math.pow(angleVec[0],2) + math.pow(angleVec[1],2)))
# # print(math.acos(arccos))
# angle = math.degrees(math.acos(arccos))
# if angleVec[1] < 0:
#     angle *= -1

# print(angle)


# def foo():
#     return 5,3

# print(type(foo()))



# print(unitVec((-10,0)))

# print(unitVecKeepSpeed((3,4),1.517))
# print(lengthVec((-2.4724901510764026, 1.3736056394868903)))


# print(unitVec(Vector2(3,4)))


# speed = Vector2(2,3)
# pos = [0,0]

# pos[0] += speed[0]
# pos[1] += speed[1]

# print(pos)


# wallStuck = "L"

# if ("L" and "R") in wallStuck:
#     print("boo")