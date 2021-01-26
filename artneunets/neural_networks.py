import numpy as np


def sigmoid(x):
    """Fonction d'activation"""
    return 1 / (1 + np.exp(-x))


class NeuNets:

    """
    Classe reseau de neurones
    La fonction 'backpropagation' n'est pas utilisee dans le projet
    mais elle est tout de meme implementee
    """

    def __init__(self, params_ai: dict) -> None:
        self.eta = params_ai["eta"]  # Parametre d'apprentissage
        self._input = []
        self._output = []
        layers = params_ai["layers"]
        self.hidden_layers = [None for _ in range(len(layers) - 2)]
        shapes = ((layers[i], layers[i + 1]) for i in range(len(layers) - 1))

        # Initialisation des poids de maniere aleatoire entre -2.5 et 2.5
        borne_inf, borne_sup = (-2.5, 2.5)
        a, b = borne_sup - borne_inf, borne_inf
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
        """Fonction de calcul de la sortie du reseau de neurones"""
        self._input = _input
        self.hidden_layers[0] = sigmoid(np.dot(self._input, self[0]))
        for i in range(1, len(self.hidden_layers)):
            matrix = np.dot(self.hidden_layers[i - 1], self[i])
            self.hidden_layers[i] = sigmoid(matrix)
        self._output = sigmoid(np.dot(self.hidden_layers[-1], self[-1]))

    def backpropagation(self, y):
        """Fonction de retropropagation du reseau de neurones"""
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
