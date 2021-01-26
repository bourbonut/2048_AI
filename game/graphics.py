# Interface du jeu

import pygame
from pathlib import Path


class Interface:

    """
    Classe Interface du jeu 2048
    """

    PATH = Path(__file__).parents[1].absolute() / "images"

    def __init__(self):
        # Initialise les directions pour l'animation
        self.directions = {
            1: self.vectors((-100, 0), lambda p: (p, 0)),  # Droite
            -1: self.vectors((100, 0), lambda p: (-p, 0)),  # Gauche
            4: self.vectors((0, -100), lambda p: (0, p)),  # Bas
            -4: self.vectors((0, 100), lambda p: (0, -p)),  # Haut
        }

        # Liste des couples de points pour les emplacements d'images
        self.emplacements = [
            (15 + 121 * ligne, 15 + 121 * colonne)
            for colonne in range(4)
            for ligne in range(4)
        ]

        # Initialisation de l'afficheur
        pygame.display.init()
        taille = longueur, hauteur = (500, 500)
        # Initialisation de la fenetre
        self.win = pygame.display.set_mode(taille)
        pygame.display.set_caption("2048")

        # Ouverture de toutes les images
        load_image = lambda e: pygame.image.load(str(self.PATH / e)).convert_alpha()
        self.background = load_image("background.png")
        self.image_game_over = load_image("game_over.png")
        self.images = {2 ** i: load_image(f"number{2**i}.png") for i in range(1, 12)}
        self.images[0] = load_image(f"number0.png")

        # Set du background
        self.win.blit(self.background, (0, 0))
        self.flip()

    def vectors(self, translation_vector: tuple, zero: tuple) -> callable:
        """Genere les fonctions utiles pour les directions"""
        translation = lambda v: (
            v[0] + translation_vector[0],
            v[1] + translation_vector[1],
        )
        return lambda v, p: (translation(v), zero(p))

    def blit(self, n_image: int, position: int) -> None:
        """Dessine l'image suivant l'emplacement"""
        self.win.blit(self.images[n_image], self.emplacements[position])

    def update(self, position: int) -> None:
        """Met a jour une partie de l'ecran"""
        coords = self.emplacements[position]
        pygame.display.update(pygame.Rect(coords[0], coords[1], 107, 107))

    def flip(self):
        """Met a jour tout l'ecran"""
        pygame.display.flip()

    def game_over(self):
        """Affiche l'ecran de fin du jeu (game over)"""
        self.win.blit(self.image_game_over, (0, 0))
        self.flip()

    def animation(self, image: int, position: int, direction: int) -> None:
        """direction = Case suivante - Case précédente"""
        # d comme départ et c comme coeffient
        translation = lambda d, c: (d[0] + c[0], d[1] + c[1])
        depart = self.emplacements[position - direction]
        arrivee = self.emplacements[position]
        param = 10  # parametre de fluidite (plus petit, plus animation fluide)
        coords, vecteur = self.directions[direction](arrivee, param)
        self.win.blit(self.background, (0, 0))
        pygame.display.update(pygame.Rect(depart[0], depart[1], 107, 107))
        for i in range(100 // param):
            self.win.blit(self.images[image], coords)
            pygame.display.update(pygame.Rect(coords[0], coords[1], 107, 107))
            self.win.blit(self.background, (0, 0))
            # parametre de vitesse (plus grand, plus vitesse lente)
            pygame.time.delay(4)
            pygame.display.update(pygame.Rect(coords[0], coords[1], 107, 107))
            coordonnees = translation(coords, vecteur)
