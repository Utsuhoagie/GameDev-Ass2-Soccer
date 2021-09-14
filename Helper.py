from pygame import *

def reflectVec(v1: tuple, n: tuple) -> tuple:
    # note that n is normed <=> n = (1,0) | (-1,0) | ...
    v2 = Vector2(v1).reflect(n)
    return v2

def lengthVec(v: tuple) -> float:
    return Vector2(v).length()

def unitVecKeepSpeed(v: tuple, speed: float) -> tuple:
    if v.length() != 0:
        return Vector2(v[0]*speed/v.length(), v[1]*speed/v.length())
    else:
        return Vector2(v[0]*speed/(v.length() + 0.1), v[1]*speed/(v.length() + 0.1))