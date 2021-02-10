import numpy as np
import math
import time
import random
import traceback
np.random.seed(int(time.time()))
random.seed(int(time.time()))


def relu(inputs):
    return np.maximum(0, inputs)


def sigmoid(inputs):
    return [1 / (1 + math.exp(-x)) for x in inputs]


class LayerDense:
    def __init__(self, n_inputs=0, n_neurons=0, activation='relu'):
        if n_inputs and n_neurons:
            self.weights = 0.1 * np.random.randn(n_inputs, n_neurons)
            self.biases = np.zeros(n_neurons)
        else:
            self.weights = []
            self.biases = []
        self.output = []

        self.activation = activation

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights)
        self.output += np.array(self.biases)

    def activate(self):
        self.output = eval(self.activation)(self.output)

    @staticmethod
    def single_point_crossover(a, b, x):
        return np.append(a[:x], b[x:]).copy(), np.append(b[:x], a[x:])

    def crossover(self, partner):

        child1 = LayerDense()
        child2 = LayerDense()
        child1.weights, child2.weights = self.cross_weights(partner.weights)

        x = random.randint(0, len(self.biases))
        child1.biases, child2.biases = self.single_point_crossover(self.biases, partner.biases, x)

        return child1, child2

    def cross_weights(self, weights):
        new_a = []
        new_b = []
        for my_neuron, partner_neuron in zip(np.array(self.weights), weights):
            x = random.randint(0, np.array(self.weights).shape[1])
            temp_a, temp_b = self.single_point_crossover(my_neuron, partner_neuron, x)
            new_a.append(temp_a)
            new_b.append(temp_b)
        return np.array(new_a), np.array(new_b)

    def mutate(self, mutation_rate):
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                rand = random.uniform(0, 100)
                if rand < mutation_rate:
                    self.weights[i][j] += random.uniform(-0.5, 0.5)

                    if self.weights[i][j] > 1:
                        self.weights[i][j] = 1

                    if self.weights[i][j] < -1:
                        self.weights[i][j] = -1

    def copy(self, other):
        self.weights = other.weights.copy()
        self.biases = other.biases.copy()
        self.activation = other.activation

