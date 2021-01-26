from game.program2048 import Game2048


def copy(*args):
    if len(args) == 1:
        return type(args[0])(args[0])
    else:
        return (type(item)(item) for item in args)


class DecisionAI(Game2048):

    """
    Classe Intelligence Artificielle basee sur les algorithmes de decisions suivants:
    | - minimax
    | - alphabeta
    | - expectiminimax

    Une derniere idee a implementer serait de faire
    augmenter la varariable 'depth' en fonction de la difficulte.
    Plus le jeu a un score eleve, plus la valeur de 'depth' augmentera.
    """

    WEIGHTS = [4 ** i for i in (15, 14, 13, 12, 8, 9, 10, 11, 7, 6, 5, 4, 0, 1, 2, 3)]

    def __init__(self):
        Game2048.__init__(self)
        self.time = 30
        self.all_moves = [self.up, self.left, self.down, self.right]
        self.algorithms = {
            "minimax": self.minimax,
            "alphabeta": self.alphabeta,
            "expectiminimax": self.expectiminimax,
        }

    def start(self, depth: int, solver: str = "minimax") -> None:
        """
        Permet de jouer a 2048 selon le solver choisi.
        Le solver peut prendre les valeurs suivantes:
        | - minimax
        | - alphabeta
        | - expectiminimax
        """
        algorithm = self.algorithms[solver]
        myfunction = lambda: self.playing(depth, algorithm)
        self.generic_start(function=myfunction, ending=False)

    def playing(self, depth: int, function: callable) -> None:
        """Fonction utilisee pendant que le jeu 2048 fonctionne"""
        self.graphism = False
        self.depth = depth
        function(depth)
        self.graphism = True
        if self.move():
            self.real_move(rd=True)

    def minimax(self, depth: int, node: str = "max") -> int:
        """
        Fonction minimax:
        | Maximise le score en minimisant les pertes lorsque
        | un nombre (2 ou 4) apparait aleatoirement
        """
        if depth == 0 or not (self.move()):
            return self.score

        elif node == "max":
            grille, zeros, score = copy(self.grille, self.zero, self.score)
            maxi = -100000
            for move in self.all_moves:
                if move(rd=False):
                    tps = self.minimax(depth - 1, "min")
                    if tps > maxi:
                        maxi = tps
                        if depth == self.depth:
                            self.real_move = move
                    self.grille, self.zero, self.score = copy(grille, zeros, score)
            return maxi

        elif node == "min":
            grille, zeros, score = copy(self.grille, self.zero, self.score)
            mini = 100000
            for x in zeros:
                for item in (2, 4):
                    self.grille[x] = item
                    self -= x
                    tps = self.minimax(depth - 1, "max")
                    if tps < mini:
                        mini = tps
                    self.grille, self.zero, self.score = copy(grille, zeros, score)
            return mini

    def alphabeta(
        self, depth: int, alpha: int = -100000, beta: int = 100000, node: str = "max"
    ) -> int:
        """
        Fonction alphabeta plus optimise que minimax:
        | Maximise le score en minimisant les pertes lorsque
        | un nombre (2 ou 4) apparait aleatoirement
        """
        if depth == 0 or not (self.move()):
            return self.score

        elif node == "max":
            grille, zeros, score = copy(self.grille, self.zero, self.score)
            tps = -100000
            for move in self.all_moves:
                if move(rd=False):
                    comparaison = int(tps)
                    tps = max(tps, self.alphabeta(depth - 1, alpha, beta, "min"))
                    if depth == self.depth and comparaison != tps:
                        self.real_move = move
                    if tps >= beta:
                        return tps
                    alpha = max(alpha, tps)
                self.grille, self.zero, self.score = copy(grille, zeros, score)

        elif node == "min":
            grille, zeros, score = copy(self.grille, self.zero, self.score)
            tps = 100000
            for x in zeros:
                for y in [2, 4]:
                    self.grille[x] = y
                    self -= x
                    tps = min(tps, self.alphabeta(depth - 1, alpha, beta, "max"))
                    if alpha >= tps:
                        return tps
                    beta = min(beta, tps)
                    self.grille, self.zero, self.score = copy(grille, zeros, score)

        return tps

    def expectiminimax(self, depth: int, chance: int = 0, node: str = "max") -> int:
        """
        Fonction expectiminimax:
        | Maximise le score avec des poids pour forcer les mouvements de maniere
        | a ce que le jeu forme un serpentin tout en minimisant les pertes lorsque
        | un nombre (2 ou 4) apparait aleatoirement
        """
        if depth == 0 or not (self.move()):
            return sum((x * y for x, y in zip(self.WEIGHTS, self.grille)))

        elif node == "max":
            grille, zeros, score = copy(self.grille, self.zero, self.score)
            maxi = -(10 ** 100)
            for move in self.all_moves:
                if move(rd=False):
                    tps = self.expectiminimax(depth - 1, node="chance")
                    if tps > maxi:
                        maxi = tps
                        if depth == self.depth:
                            self.real_move = move
                    self.grille, self.zero = copy(grille, zeros)
            return maxi

        elif node == "min":
            grille, zeros, score = copy(self.grille, self.zero, self.score)
            mini = 10 ** 100
            for y in (2, 4):
                self.grille[chance] = y
                self -= chance
                tps = self.expectiminimax(depth - 1, node="max")
                if tps < mini:
                    mini = tps
                self.grille, self.zero = copy(grille, zeros)
            return mini

        elif node == "chance":
            zeros = copy(self.zero)
            average = [self.expectiminimax(depth, c, node="min") for c in zeros]
            return sum(average) / len(average)


if __name__ == "__main__":
    ai = DecisionAI()
    ai.start(depth=4, solver="minimax")
