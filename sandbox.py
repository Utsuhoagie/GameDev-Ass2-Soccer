import math
import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            angle_between((1, 0, 0), (1, 0, 0))
            0.0
            angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def reverseVec(vec: tuple):
    vec = (-vec[0], -vec[1])
    #print(vec)

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

vec = (2,2)
n = (0,-1)
# vec2 = (3,1)
# print(reflectVec(vec,n))
reverseVec(vec)


# print(str(abs(-5)))



angleVec = (4,4)
arccos = float(angleVec[0]/math.sqrt(math.pow(angleVec[0],2) + math.pow(angleVec[1],2)))
# print(math.acos(arccos))
angle = math.degrees(math.acos(arccos))
if angleVec[1] < 0:
    angle *= -1

print(angle)


# def foo():
#     return 5,3

# print(type(foo()))