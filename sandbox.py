import math
import random


def sigmoid(inputs):
    return [1 / (1 + math.exp(-x)) for x in inputs]


for _ in range(10000):
    print(random.uniform(0, 100))
