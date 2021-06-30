# Interface du jeu

import pygame
from copy import copy
from pygame.math import Vector2 as vec2
from pathlib import Path
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

colors = yaml.load(stream=open("colors.yaml", "r"), Loader=Loader)


def sprite(number: int) -> pygame.Surface:
    """
    Generate a surface with the right color and the number written
    """
    color, size, font_color = colors[number]
    sprite = pygame.Surface((107, 107), pygame.SRCALPHA)
    sprite.convert_alpha()
    pygame.draw.rect(sprite, color, pygame.Rect(0, 0, 107, 107), border_radius=5)
    font = pygame.font.Font("clear-sans.bold.ttf", size)
    text = font.render(f"{number}", True, font_color)
    w, h = text.get_rect().center
    sprite.blit(text, ((53 - w, 53 - h - 5)))
    return sprite


def background(locations: list) -> pygame.Surface:
    """
    Generate the background of the game
    """
    background = pygame.Surface((500, 500))
    background.fill(colors[-1][0])
    color = colors[0][0]
    for location in locations:
        rect = pygame.Rect(location, (107, 107))
        pygame.draw.rect(background, color, rect, border_radius=5)
    return background


def gameover() -> pygame.Surface:
    """
    Generate the gameover surface
    """
    gameover = pygame.Surface((500, 500))
    gameover.set_alpha(120)
    font = pygame.font.Font("clear-sans.bold.ttf", 56)
    text = font.render("Game over", True, [255, 0, 0])
    w, h = text.get_rect().center
    gameover.blit(text, ((250 - w, 250 - h - 5)))
    return gameover


class Interface:

    """
    Graphic interface for 2048 game
    """

    NB_I = 20  # number of how many images will be drawn for an animation
    NB_H = 20  # number of how many homotheties will be applied for a new number after an addition
    FPS = 240  # Frames per second

    def __init__(self):
        # List of vectors for locations of images
        self.locations = [
            vec2(15 + 121 * ligne, 15 + 121 * colonne)
            for colonne in range(4)
            for ligne in range(4)
        ]

        pygame.init()
        self.win = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("2048")

        # Draw all images
        self.background = background(self.locations)
        self.images = {0: sprite(0)}
        self.images.update({2 ** i: sprite(2 ** i) for i in range(1, 18)})
        self.gameover = gameover()

        # Set background
        self.win.blit(self.background, (0, 0))
        self.flip()

        # Some useful parameters
        self.moves, self.additions = [], []
        self.before, self.after = [], []
        self.clock = pygame.time.Clock()

    def blit(self, n_image: int, position: int) -> None:
        """Draw the image `n_image` according to the `position`"""
        self.win.blit(self.images[n_image], self.locations[position])

    def update(self, position: int) -> None:
        """Update a part of the screen"""
        coords = self.locations[position]
        pygame.display.update(pygame.Rect(coords[0], coords[1], 107, 107))

    def flip(self):
        """Update all the screen"""
        pygame.display.flip()

    def game_over(self):
        """Display the game over image on the screen"""
        self.win.blit(self.gameover, (0, 0))
        self.flip()

    def update_moves(self, directions):
        for direction in directions:
            before = [self.before[i] for i in direction]
            after = [self.after[i] for i in direction]
            self.moving(before, after, direction)

    def moving(self, before: list, after: list, direction: list) -> None:
        """Find moves and additions for animations and store them in `moves` and `additions`"""
        i = 3
        while i > -1:
            if not after[i]:
                break
            elif after[i] == before[i]:
                i -= 1
                continue
            reference, j = after[i], i
            while j > -1:
                item = before[j]
                if item == reference:
                    self.moves.append([direction[j], direction[i], before[j]])
                    break

                elif item and item < reference:
                    k, found = 1, False
                    while k < j + 1:
                        if before[j - k] and before[j - k] != item:
                            break
                        elif before[j - k] == item:
                            self.additions.append([direction[i], reference])
                            if i != j:
                                self.moves.append([direction[j], direction[i], item])
                            self.moves.append([direction[j - k], direction[i], item])
                            before = before[: j - k] + [0] * (4 - j + k)
                            found = True
                            break
                        k += 1
                    if found:
                        break
                j -= 1
            i -= 1

    def reset_animation(self):
        """Reset animation lists"""
        self.moves = []
        self.additions = []

    def setbefore(self, before: list):
        """Set `before` list"""
        self.before = copy(before)

    def setafter(self, after: list):
        """Set `after` list"""
        self.after = copy(after)

    def allmovements(self):
        """
        Generate a list `movements` which, for all movements, contains:
            - the image of the number which will move
            - the starting position of the number
            - `q` which is the euclidian quotient of `(end - start) // nb_images`
            - `r` which is the euclidian remainder of `(end - start) % nb_images`
            - `symbol` which is 1 if end > start else -1

        Notes:
            `pygame` offers the class `Vector2` which in my opinion, is not complete.
            You can try euclidian division but it will not return the expected result.
            For instance:
            ```
            >>> (end - start)//20
            <Vector2(-13, 0)>
            >>> (378-136)//20
            12
            ```
            In addition, the class doesn't support the operator `%`.
        """
        self.movements = []
        for start, end, number in self.moves:
            symbol = 1 if end > start else -1
            start = self.locations[start]
            end = self.locations[end]
            diff = end - start
            q = vec2(diff[0] // self.NB_I, diff[1] // self.NB_I)
            r = vec2(diff[0] % self.NB_I, diff[1] % self.NB_I)
            r = r / self.NB_I
            limits = vec2((107, 107)) + 2 * symbol * q
            data = (start, limits, q, r, symbol)
            self.movements.append([self.images[number], data])

    def allscales(self):
        """
        Generate a dictionary `allscales` where:
            - the key is the number
            - the value is a list of a succession of images of the number
              with different font size
        Note:
            The first element of each list is the number with a font size equal to 0,
            so without text.
        """
        self.scales = {}
        for number in {number for _, number in self.additions}:
            color, size, font_color = colors[number]
            images = []
            q, r = size // self.NB_H, (size % self.NB_H) / self.NB_H

            for s in range(self.NB_H + 1):
                image = pygame.Surface((107, 107), pygame.SRCALPHA)
                image.convert_alpha()
                region = pygame.Rect(0, 0, 107, 107)
                pygame.draw.rect(image, color, region, border_radius=5)
                font = pygame.font.Font("clear-sans.bold.ttf", s * q + int(s * r))
                text = font.render(f"{number}", True, font_color)
                w, h = text.get_rect().center
                image.blit(text, ((53 - w, 53 - h - 5)))
                images.append(image)
            self.scales[number] = images

    def animation(self, directions: list) -> None:
        """
        Manage all animations of the game
        """
        self.update_moves(directions)
        self.allscales()
        self.allmovements()
        for i in range(self.NB_I + 1):
            self.clock.tick(self.FPS)
            self.win.blit(self.background, (0, 0))
            regions = []

            for images, data in self.movements:
                start, limits, q, r, symbol = data
                vec = start + i * q + vec2(int(i * r[0]), int(i * r[1]))
                self.win.blit(images, vec)
                k = (i - 1) if symbol > 0 else i
                vec = start + k * q + vec2(int(k * r[0]), int(k * r[1]))
                regions.append(pygame.Rect(vec, limits))

            for pos, number in self.additions:
                image = self.scales[number][0]
                self.win.blit(image, self.locations[pos])
                regions.append(pygame.Rect(self.locations[pos], (107, 107)))

            pygame.display.update(regions)

        for i in range(0, self.NB_I + 1):
            regions = []
            for pos, number in self.additions:
                image = self.scales[number][i]
                self.win.blit(image, self.locations[pos])
                regions.append(pygame.Rect(self.locations[pos], (107, 107)))
            pygame.display.update(regions)

        self.reset_animation()
