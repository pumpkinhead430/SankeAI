import math
import pygame
import numpy as np
import time
def sigmoid(inputs):
    return [1 / (1 + math.exp(-x)) for x in inputs]


vect = pygame.Vector2(0, 21)
vect2 = pygame.Vector2(0, 20)
print(1 / vect.distance_to(vect2))

