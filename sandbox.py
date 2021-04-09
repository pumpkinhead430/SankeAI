import math
import pygame
import numpy as np
import time


def sigmoid(inputs):
    return [1 / (1 + math.exp(-x)) for x in inputs]

vect1 = pygame.Vector2(1, 0)
vect2 = vect1
vect2 *= 6
print(vect1)
