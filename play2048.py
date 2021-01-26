# Jouer a 2048

from game.program2048 import Game2048


class MyGame(Game2048):

    """Classe pour jouer au jeu 2048"""

    def __init__(self):
        Game2048.__init__(self)

    def start(self):
        self.generic_start(function=self.play, ending=True)


if __name__ == "__main__":
    game = MyGame()
    game.start()
