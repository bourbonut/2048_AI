from game.program2048 import Game2048
from .neural_networks import NeuNets
import pygame
import numpy as np
from random import choice


class ArtInt(NeuNets):

    """Artificial Intelligence class with neural network"""

    def __init__(self, params_ai):
        NeuNets.__init__(self, params_ai)
        self.params_ai = params_ai
        self.time = 30
        self.game = Game2048()
        self.score = self.game.score
        self.algorithms = {"basic": self.basic_output, "advanced": self.advanced_output}

    def __copy__(self):
        new = ArtInt(self.params_ai)
        new.weights = list(self.weights)
        new.score = int(self.game.score)
        return new

    def __str__(self):
        return f"IA = ({self.score = })"

    def __repr__(self):
        return str(self)

    def ai_start(self, solver: str = "basic") -> None:
        self.game.restart()
        algorithm = self.algorithms[solver]
        myfunction = lambda: self.playing(algorithm)
        self.game.generic_ai_start(function=myfunction)
        self.score = self.game.score

    def start(self, solver: str = "basic") -> None:
        self.game.restart()
        algorithm = self.algorithms[solver]
        myfunction = lambda: self.playing(algorithm)
        self.game.generic_start(function=myfunction, ending=False)
        self.score = self.game.score

    def think(self, grid: list) -> list:
        """Use a neural network and return the output"""
        grid = np.log2(np.where(grid == 0, 1, grid))
        self.feedforward(grid)
        output = self._output.tolist()
        return output

    def playing(self, function: callable) -> None:
        """
        While the A.I. is blocked, it plays a direction
        that is yet tried, based on the output
        """
        output = function()
        condition = False
        while not (condition) and output.count(-1) != 4:
            i = output.index(max(output))
            condition = self.game.action(self.game.actionkeys[i])
            output[i] = -1

    def basic_output(self):
        """Use the neural network et return the output depending of the situation of the game"""
        return self.think(np.array(self.game.grid))

    def advanced_output(self):
        """Check if the A.I. gives the same result when a rotation of the game grid is done"""
        grid = np.array(self.game.grid)
        grid_h = np.flipud(grid.reshape(4, 4))
        grid_v = np.fliplr(grid.reshape(4, 4))

        output_h = self.think(grid_h.reshape(1, 16))[0]
        output_v = self.think(grid_v.reshape(1, 16))[0]
        output_h[0], output_h[2] = output_h[2], output_h[0]
        output_v[1], output_v[3] = output_v[3], output_v[1]

        liste_outputs = np.array([self.think(grid), output_h, output_v])
        liste_outputs = np.array(liste_outputs)

        output_final = sum(liste_outputs) / 3
        return output_final.tolist()
