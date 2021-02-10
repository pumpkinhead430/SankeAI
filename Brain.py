from Layer_Dense import LayerDense
from CONSTANTS import look_size
hidden_neuron_amount = 8
input_amount = 24
output_amount = 4


class Brain:

    def __init__(self):
        self.inputs = []
        self.hidden_layers = []
        self.hidden_layers.append(LayerDense(input_amount, hidden_neuron_amount))
        self.hidden_layers.append(LayerDense(hidden_neuron_amount, hidden_neuron_amount))
        self.output_layer = LayerDense(hidden_neuron_amount, output_amount, 'sigmoid')

    def think(self):
        self.hidden_layers[0].forward(self.inputs)
        self.hidden_layers[0].activate()
        self.hidden_layers[1].forward(self.hidden_layers[0].output)
        self.hidden_layers[1].activate()
        self.output_layer.forward(self.hidden_layers[1].output)
        self.output_layer.activate()

    def crossover(self, partner):
        child1 = Brain()
        child2 = Brain()
        for i in range(len(child1.hidden_layers)):
            child1.hidden_layers[i], child2.hidden_layers[i] = self.hidden_layers[i].crossover(partner.hidden_layers[i])
        return child1, child2

    def mutate(self, mutation_rate):
        for layer in self.hidden_layers:
            layer.mutate(mutation_rate)

    def copy(self, other):
        for my_layer, other_layer in zip(self.hidden_layers, other.hidden_layers):
            my_layer.copy(other_layer)



