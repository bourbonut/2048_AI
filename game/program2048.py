# jeu 2048

from game.graphics import Interface

from random import choice
from random import randint
from random import random
import pygame
import os


class Game2048:

    """
    Jeu generique 2048
    """

    LIGNE = {0: [0, 1, 2, 3], 1: [4, 5, 6, 7], 2: [8, 9, 10, 11], 3: [12, 13, 14, 15]}
    INV_LIGNE = {
        0: [3, 2, 1, 0],
        1: [7, 6, 5, 4],
        2: [11, 10, 9, 8],
        3: [15, 14, 13, 12],
    }
    COLONNE = {0: [0, 4, 8, 12], 1: [1, 5, 9, 13], 2: [2, 6, 10, 14], 3: [3, 7, 11, 15]}
    INV_COLONNE = {
        0: [12, 8, 4, 0],
        1: [13, 9, 5, 1],
        2: [14, 10, 6, 2],
        3: [15, 11, 7, 3],
    }

    def __init__(self):
        self.grille = [0 for i in range(16)]
        self.zero = list(range(16))
        self.score = 0
        self.movements = {
            -4: self.movement_condition(self.LIGNE[0], -4),  # Haut
            4: self.movement_condition(self.LIGNE[3], 4),  # Bas
            -1: self.movement_condition(self.COLONNE[0], -1),  # Gauche
            1: self.movement_condition(self.COLONNE[3], 1),  # Droite
        }
        self.time = 60

    def __len__(self):
        return len(self.grille)

    def __getitem__(self, key):
        return self.grille[key]

    def __setitem__(self, key, item):
        self.grille[key] = item

    def __iadd__(self, item):
        """Uniquement pour la liste des zéros"""
        self.zero.append(item)
        return self

    def __isub__(self, item):
        """Uniquement pour la liste des zéros"""
        self.zero.remove(item)
        return self

    def __repr__(self):
        return "\n".join((str(self[4 * i : 4 * (i + 1)]) for i in range(4)))

    def restart(self) -> None:
        """Recommence le jeu"""
        self.grille = [0 for i in range(16)]
        self.zero = list(range(16))
        self.score = 0

    def set_first_elements(self) -> None:
        """Initialise les premiers elements de jeu"""
        a, b, c = randint(0, 15), randint(0, 15), randint(0, 15)
        self[a], self[b], self[c] = (self.random_2_4() for _ in range(3))
        self -= a
        if a != b:
            self -= b
        if a != c and b != c:
            self -= c
        if self.graphism:
            self.interface = Interface()
            for i in range(16):
                self.update(i)

    def generic_start(self, function: callable, ending: bool = False) -> None:
        """
        Permet de jouer selon la fonction 'function' avec l'interface graphique.
        Si 'ending' faux, le jeu se ferme directement apres le game over
        """
        self.graphism = True
        self.set_first_elements()
        self.run = True
        while self.move() and self.run:
            while self.zero and self.run:
                self.is_running()
                function()
            self.is_running()
            function()
        if self.run:
            for i in range(16):
                self.update(i)
            self.interface.game_over()
            if ending:
                while self.run:
                    self.is_running()
        pygame.quit()

    def generic_ai_start(self, function: callable) -> None:
        """Permet de jouer selon la fonction 'function' sans l'interface graphique"""
        self.graphism = False
        self.set_first_elements()
        while self.move():
            while self.zero:
                function()
            function()

    def is_running(self) -> None:
        """Code pour pouvoir fermer la fenetre"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def random_2_4(self) -> int:
        """Genere aleatoirement un 2 (probabilite:0.8) ou un 4 (probabilite:0.2)"""
        return 2 if random() <= 0.8 else 4

    def move_zero(self, liste: list) -> None:
        """Cherche le premier zero puis lance 'moving'"""
        index = 3
        arrive = 0
        while self[liste[arrive]] != 0 and index > -1:
            arrive = index
            index -= 1
        if index == -1:
            return
        else:
            self.moving(0, arrive, liste)

    def moving(self, depart: int, arrive: int, liste: list) -> None:
        """Deplace les zeros et les nombres normaux"""
        suivant = depart + 1
        if suivant > 3:
            return
        elif self[liste[suivant]] != 0:
            self.moving(suivant, arrive, liste)
        elif self[liste[suivant]] == self[liste[depart]]:
            self.moving(suivant, arrive, liste)
        else:
            self[liste[depart]], self[liste[suivant]] = (
                self[liste[suivant]],
                self[liste[depart]],
            )
            self -= liste[suivant]
            self += liste[depart]
            if self.graphism:
                self.animation(liste[suivant], liste[depart])
            if depart > 0 and self[liste[depart - 1]] != 0:
                self.moving(depart - 1, arrive, liste)
            else:
                self.moving(suivant, arrive, liste)

    def comparaison(self, liste: list) -> None:
        """Additionne les cases si possible"""
        for i in range(3):
            depart, arrivee = liste[i], liste[i + 1]
            if self[depart] != 0 and self[depart] == self[arrivee]:
                self[depart] += self[depart]
                self.score += self[depart]
                self[arrivee] = 0
                self += arrivee
                if self.graphism:
                    self.animation(depart, arrivee)

    def animation(self, arrivee: int, depart: int, debug=False) -> None:
        """
        Met a jour les elements lors d'une action
        (generalement 'up','down','left','right')
        Si 'debug' vaut False, une animation de deplacement des nombres est permise
        """
        if not (debug):
            self.interface.animation(self[arrivee], arrivee, arrivee - depart)
        self.update(depart)
        self.update(arrivee)

    def update(self, position: int) -> None:
        """Met a jour l'objet de la grille à la position donnee"""
        self.interface.blit(self[position], position)
        self.interface.update(position)

    def random(self) -> None:
        """Genere un nombre (2 ou 4) et le met a jour graphiquement"""
        r = choice(self.zero)
        self.grille[r] = self.random_2_4()
        self -= r
        if self.graphism:
            self.update(r)

    def up(self, rd: bool = True) -> bool:
        """Mouvement haut"""
        if self.partial_move(-4):
            for i in range(4):
                self.move_zero(self.INV_COLONNE[i])
            for i in range(4):
                self.comparaison(self.COLONNE[i])
            for i in range(4):
                self.move_zero(self.INV_COLONNE[i])

            if rd:
                self.random()
            return True

    def down(self, rd: bool = True) -> bool:
        """Mouvement bas"""
        if self.partial_move(4):
            for i in range(4):
                self.move_zero(self.COLONNE[i])
            for i in range(4):
                self.comparaison(self.INV_COLONNE[i])
            for i in range(4):
                self.move_zero(self.COLONNE[i])

            if rd:
                self.random()
            return True

    def right(self, rd: bool = True) -> bool:
        """Mouvement droite"""
        if self.partial_move(1):
            for i in range(4):
                self.move_zero(self.LIGNE[i])
            for i in range(4):
                self.comparaison(self.INV_LIGNE[i])
            for i in range(4):
                self.move_zero(self.LIGNE[i])

            if rd:
                self.random()
            return True

    def left(self, rd: bool = True) -> bool:
        """Mouvement gauche"""
        if self.partial_move(-1):
            for i in range(4):
                self.move_zero(self.INV_LIGNE[i])
            for i in range(4):
                self.comparaison(self.LIGNE[i])
            for i in range(4):
                self.move_zero(self.INV_LIGNE[i])

            if rd:
                self.random()
            return True

    def move(self) -> bool:
        """Verifie si l'on peut continuer à jouer"""
        if len(self.zero) != 0:
            return True
        i = 0
        condition = False
        bordure_droite = [3, 7, 11]
        bordure_bas = [12, 13, 14]
        while i < 15 and not (condition):
            if i in bordure_droite:
                if self[i] == self[i + 4]:
                    condition = True
                else:
                    i += 1
            elif i in bordure_bas:
                if self[i] == self[i + 1]:
                    condition = True
                else:
                    i += 1
            elif self[i] == self[i + 1] or self[i] == self[i + 4]:
                condition = True
            else:
                i += 1
        return condition

    def movement_condition(self, l: list, n: int) -> callable:
        """Genere une fonction condition utile pour la fonction 'partial_move'"""
        return lambda i: not (i in l) and (self[i] == self[i + n] or self[i + n] == 0)

    def partial_move(self, movement: int) -> bool:
        """Verifie si le mouvement est jouable"""
        liste = [i for i in range(16) if not (i in self.zero)]
        condition = False
        j = 0
        while j < len(liste) and not (condition):
            i = liste[j]
            if self.movements[movement](i):
                condition = True
            else:
                j += 1
        return condition

    def play(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.up()
            pygame.time.delay(self.time)
        elif keys[pygame.K_DOWN]:
            self.down()
            pygame.time.delay(self.time)
        elif keys[pygame.K_LEFT]:
            self.left()
            pygame.time.delay(self.time)
        elif keys[pygame.K_RIGHT]:
            self.right()
            pygame.time.delay(self.time)


if __name__ == "__main__":
    game = Game2048()
    game.start()
