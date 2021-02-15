import math
import pygame
import time
import numpy as np
def sigmoid(inputs):
    return [1 / (1 + math.exp(-x)) for x in inputs]

help = np.zeros((20, 19))
print(help.shape[1])

