import math


def sigmoid(inputs):
    return [1 / (1 + math.exp(-x)) for x in inputs]


print(sigmoid([0, 432, -6, 1, 5]))
