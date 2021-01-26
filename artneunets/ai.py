from game.program2048 import Game2048
from artneunets.neural_networks import NeuNets
import pygame
import numpy as np
from random import choice


class ArtInt(NeuNets):

    """Classe intelligence artificielle avec un reseau de neurones"""

    def __init__(self, params_ai):
        NeuNets.__init__(self, params_ai)
        self.params_ai = params_ai
        self.time = 30
        self.game = Game2048()
        self.score = self.game.score
        self.all_moves = [self.game.up, self.game.left, self.game.down, self.game.right]
        self.algorithms = {"basic": self.basic_output, "advanced": self.advanced_output}

    def __copy__(self):
        new = ArtInt(self.params_ai)
        new.weights = list(self.weights)
        new.score = int(self.game.score)
        return new

    def __str__(self):
        return f"IA = (score = {self.score})"

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

    def think(self, grille: list) -> list:
        """Utilise le reseau de neurones et renvoie sa sortie"""
        grille = np.log2(np.where(grille == 0, 1, grille))
        self.feedforward(grille)
        output = self._output.tolist()
        return output

    def playing(self, function: callable) -> None:
        """
        Tant que l'IA est bloquee, elle joue une direction
        qu'elle n'a pas encore essayee, basee sur sa sortie
        """
        output = function()
        condition = False
        while not (condition) and output.count(-1) != 4:
            i = output.index(max(output))
            condition = self.all_moves[i]()
            output[i] = -1

    def basic_output(self):
        """Utilise le reseau de neurones et renvoie sa sortie en fonction de l'etat du jeu"""
        return self.think(np.array(self.game.grille))

    def advanced_output(self):
        """Vérifie si l'IA donne le meme résultat en faisant une rotation de la grille de jeu"""
        grille = np.array(self.game.grille)
        grille_h = np.flipud(grille.reshape(4, 4))
        grille_v = np.fliplr(grille.reshape(4, 4))

        output_h = self.think(grille_h.reshape(1, 16))[0]
        output_v = self.think(grille_v.reshape(1, 16))[0]
        output_h[0], output_h[2] = output_h[2], output_h[0]
        output_v[1], output_v[3] = output_v[3], output_v[1]

        liste_outputs = np.array([self.think(grille), output_h, output_v])
        liste_outputs = np.array(liste_outputs)

        output_final = sum(liste_outputs) / 3
        return output_final.tolist()
