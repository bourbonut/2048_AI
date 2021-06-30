import numpy as np


def sigmoid(x):
    """Function of activation"""
    return 1 / (1 + np.exp(-x))


class NeuNets:

    """
    Neural networks class
    The function 'backpropagation' is not used in this project
    but it is implemented anyway
    """

    def __init__(self, params_ai: dict) -> None:
        self.eta = params_ai["eta"]  # Learning parameter
        self._input = []
        self._output = []
        layers = params_ai["layers"]
        self.hidden_layers = [None for _ in range(len(layers) - 2)]
        shapes = ((layers[i], layers[i + 1]) for i in range(len(layers) - 1))

        # Initialization of weights randomly between -2.5 and 2.5
        border_low, border_up = (-2.5, 2.5)
        a, b = border_up - border_low, border_low
        random_sample = np.random.random_sample
        self.weights = [a * random_sample(shape) + b for shape in shapes]

    def __getitem__(self, key):
        return self.weights[key]

    def __setitem__(self, key, item):
        self.weights[key] = item

    def __len__(self):
        return len(self.weights)

    def __str__(self):
        disp = f"Number of layers : {len(self) + 1}\n\nWeights:\n"
        for index, weight in enumerate(self.weights):
            disp += f"(Index: {index}; Shape: {weight.shape}):\n{weight}\n\n"
        return disp

    def __repr__(self):
        return str(self)

    def feedforward(self, _input):
        """Function to calculate the output of the neural network"""
        self._input = _input
        self.hidden_layers[0] = sigmoid(np.dot(self._input, self[0]))
        for i in range(1, len(self.hidden_layers)):
            matrix = np.dot(self.hidden_layers[i - 1], self[i])
            self.hidden_layers[i] = sigmoid(matrix)
        self._output = sigmoid(np.dot(self.hidden_layers[-1], self[-1]))

    def backpropagation(self, y):
        """backpropagation function of the neural network"""
        deltas = []
        shape = self[-1].shape
        gap = y - self._output
        matrix = gap * self._output * (np.ones(self._output.shape) - self._output)
        r_matrix = matrix.reshape((1, shape[1]))
        hidden_layer = self.hidden_layers[-1].reshape((shape[0], 1))
        deltas.append(self.eta * np.dot(hidden_layer, r_matrix))

        for i in range(1, len(self)):
            shape = self[-i].shape
            layer = self.hidden_layers[-i]
            x = self._input if i == len(self) - 1 else self.hidden_layers[-i - 1]
            m = np.dot(self[-i].reshape(shape), matrix.reshape((shape[1], 1)))
            matrix = m * (layer * (np.ones(layer.shape) - layer)).reshape((shape[0], 1))
            deltas.append(self.eta * np.dot(matrix, x.reshape((1, x.shape[0]))).T)

        deltas.reverse()
        for i, delta in enumerate(deltas):
            self[i] += delta
