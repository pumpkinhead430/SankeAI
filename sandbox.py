import math
import pygame

def sigmoid(inputs):
    return [1 / (1 + math.exp(-x)) for x in inputs]


help = pygame.Vector2(0, -20)
help = help.rotate(90)
print(help)

