# jeu 2048

from game.graphics import Interface

from random import choice
from random import randint
from random import random
import pygame
import os


class Game2048:

    """
    Generic 2048 game
    """

    ORDERS = {
        1: [[i for i in range(k * 4, k * 4 + 4)] for k in range(4)],
        -1: [[i for i in range(k * 4 + 4 - 1, k * 4 - 1, -1)] for k in range(4)],
        4: [[k + 4 * i for i in range(4)] for k in range(4)],
        -4: [[k + 4 * i for i in range(4 - 1, -1, -1)] for k in range(4)],
    }

    def __init__(self):
        self.grid = [0] * 16
        self.zero = list(range(16))
        self.score = 0

        # actionkeys and vs (order): [up, down, left, right]
        self.actionkeys = (-4, 4, -1, 1)
        vs = ([0, 1, 2, 3], [12, 13, 14, 15], [0, 4, 8, 12], [3, 7, 11, 15])  # values
        self.movements = {k: self.condition(v, k) for k, v in zip(self.actionkeys, vs)}

    def __len__(self):
        return len(self.grid)

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, item):
        self.grid[key] = item

    def __iadd__(self, item):
        """Only for zeroes list"""
        self.zero.append(item)
        return self

    def __isub__(self, item):
        """Only for zeroes list"""
        self.zero.remove(item)
        return self

    def __repr__(self):
        return "\n".join((str(self[4 * i : 4 * (i + 1)]) for i in range(4))) + "\n"

    def restart(self) -> None:
        """Restart game"""
        self.grid = [0] * 16
        self.zero = list(range(16))
        self.score = 0

    def set_first_elements(self) -> None:
        """Initialize the first elements of the game"""
        a, b, c = randint(0, 15), randint(0, 15), randint(0, 15)
        self[a], self[b], self[c] = (self.random_2_4() for _ in range(3))
        self -= a
        if a != b:
            self -= b
        if a != c and b != c:
            self -= c
        if self.graphism:
            self.interface = Interface()
            self.update_all()

    def generic_start(self, function: callable, ending: bool = False) -> None:
        """
        Allow to play according to the argument `function` with the graphic interface
        If `ending` is `False`, the game stops directly after a game over
        """
        self.graphism = True
        self.set_first_elements()
        self.run = True
        while self.move() and self.run:
            while self.zero and self.run:
                self.isrunning()
                function()
            self.isrunning()
            function()
        if self.run:
            self.update_all()
            self.interface.game_over()
            if ending:
                while self.run:
                    self.isrunning()
        pygame.quit()

    def generic_ai_start(self, function: callable) -> None:
        """Allow to play according to the argument `function` without the graphic interface"""
        self.graphism = False
        self.set_first_elements()
        while self.move():
            while self.zero:
                function()
            function()

    def isrunning(self) -> None:
        """Code to be able to close the window"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def random_2_4(self) -> int:
        """Generate randomly 2 (probability: 0.8) or 4 (probability: 0.2)"""
        return 2 if random() <= 0.8 else 4

    def move_zero(self, order: list) -> None:
        """Find the first zero and start 'moving'"""
        for list_ in order:
            index = 3
            end = 0
            while self[list_[end]] != 0 and index > -1:
                end = index
                index -= 1
            if index == -1:
                continue
            else:
                self.moving(0, end, list_)

    def moving(self, start: int, end: int, list_: list) -> None:
        """Move zeroes and numbers"""
        next_ = start + 1
        if next_ > 3:
            return
        lnext, lstart = list_[next_], list_[start]
        snext, sstart = self[lnext], self[lstart]
        if snext != 0:
            self.moving(next_, end, list_)
        elif snext == sstart:
            self.moving(next_, end, list_)
        else:
            self[lstart], self[lnext] = (snext, sstart)
            self -= lnext
            self += lstart
            if start > 0 and self[list_[start - 1]] != 0:
                self.moving(start - 1, end, list_)
            else:
                self.moving(next_, end, list_)

    def compare(self, order: list) -> None:
        """Add les cells if possible"""
        for list_ in order:
            for i in range(3):
                start, end = list_[i], list_[i + 1]
                if self[start] != 0 and self[start] == self[end]:
                    self[start] += self[start]
                    self.score += self[start]
                    self[end] = 0
                    self += end

    def before(self) -> None:
        """Only if there is an `interface`. Set the `grid` for the previous state"""
        if self.graphism:
            self.interface.setbefore(self.grid)

    def animation(self, key: int) -> None:
        """Update elements during an action `up`, `down`, `left`, `right`"""
        if self.graphism:
            self.interface.setafter(self.grid)
            self.interface.animation(self.ORDERS[key])

    def update(self, position: int) -> None:
        """Update the object on grid according to `position`"""
        self.interface.blit(self[position], position)
        self.interface.update(position)

    def update_all(self):
        for i in range(16):
            self.update(i)

    def random(self) -> None:
        """Choose randomly a number (2 ou 4) and update graphicaly"""
        r = choice(self.zero)
        self.grid[r] = self.random_2_4()
        self -= r
        if self.graphism:
            self.update(r)

    def action(self, key, rd: bool = True):
        if self.partial_move(key):
            self.before()
            self.move_zero(self.ORDERS[key])
            self.compare(self.ORDERS[-key])
            self.move_zero(self.ORDERS[key])
            self.animation(key)
            if rd:
                self.random()
            return True

    def move(self) -> bool:
        """Check if the player can play"""
        if len(self.zero) != 0:
            return True
        i = 0
        condition = False
        right_border = [3, 7, 11]
        bottom_border = [12, 13, 14]
        while i < 15 and not (condition):
            if i in right_border:
                if self[i] == self[i + 4]:
                    condition = True
                else:
                    i += 1
            elif i in bottom_border:
                if self[i] == self[i + 1]:
                    condition = True
                else:
                    i += 1
            elif self[i] == self[i + 1] or self[i] == self[i + 4]:
                condition = True
            else:
                i += 1
        return condition

    def condition(self, l: list, n: int) -> callable:
        """Generate a function useful for 'partial_move'"""
        return lambda i: not (i in l) and (self[i] == self[i + n] or self[i + n] == 0)

    def partial_move(self, movement: int) -> bool:
        """Check if the movement is playable"""
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
            self.action(-4)
        elif keys[pygame.K_DOWN]:
            self.action(4)
        elif keys[pygame.K_LEFT]:
            self.action(-1)
        elif keys[pygame.K_RIGHT]:
            self.action(1)
