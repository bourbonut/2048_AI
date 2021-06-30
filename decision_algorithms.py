from game.program2048 import Game2048


def copy(*args):
    if len(args) == 1:
        return type(args[0])(args[0])
    else:
        return (type(item)(item) for item in args)


class DecisionAI(Game2048):

    """
    Artificial Intelligence class based on the following decision algorithms:
    | - minimax
    | - alphabeta
    | - expectiminimax
    """

    # TODO: Combine alphabeta and expectiminimax
    # TODO: `depth` should increase according to the difficulty

    WEIGHTS = [4 ** i for i in (15, 14, 13, 12, 8, 9, 10, 11, 7, 6, 5, 4, 0, 1, 2, 3)]

    def __init__(self):
        Game2048.__init__(self)
        # self.all_moves = [self.up, self.left, self.down, self.right]
        self.algorithms = {
            "minimax": self.minimax,
            "alphabeta": self.alphabeta,
            "expectiminimax": self.expectiminimax,
        }

    def start(self, depth: int, solver: str = "minimax") -> None:
        """
        Function used to play 2048 according to the chosen solver.
        The solver can take the following values:
        | - minimax
        | - alphabeta
        | - expectiminimax
        """
        algorithm = self.algorithms[solver]
        myfunction = lambda: self.playing(depth, algorithm)
        self.generic_start(function=myfunction, ending=False)

    def playing(self, depth: int, function: callable) -> None:
        """Function used to make the A.I. play the game"""
        self.graphism = False
        self.depth = depth
        function(depth)
        self.graphism = True
        if self.move():
            self.action(self.real_move, rd=True)

    def minimax(self, depth: int, node: str = "max") -> int:
        """
        Function minimax:
        | Maximize the score while minimizing the losses when
        | a number (2 or 4) appears randomly
        """
        if depth == 0 or not (self.move()):
            return self.score

        elif node == "max":
            grid, zeros, score = copy(self.grid, self.zero, self.score)
            maxi = -100000
            # for move in self.all_moves:
            for key in self.actionkeys:
                if self.action(key, rd=False):
                    tps = self.minimax(depth - 1, "min")
                    if tps > maxi:
                        maxi = tps
                        if depth == self.depth:
                            self.real_move = key
                    self.grid, self.zero, self.score = copy(grid, zeros, score)
            return maxi

        elif node == "min":
            grid, zeros, score = copy(self.grid, self.zero, self.score)
            mini = 100000
            for x in zeros:
                for item in (2, 4):
                    self.grid[x] = item
                    self -= x
                    tps = self.minimax(depth - 1, "max")
                    if tps < mini:
                        mini = tps
                    self.grid, self.zero, self.score = copy(grid, zeros, score)
            return mini

    def alphabeta(
        self, depth: int, alpha: int = -100000, beta: int = 100000, node: str = "max"
    ) -> int:
        """
        Function alphabeta more optimized than minimax:
        | Maximize the score while minimizing the losses when
        | a number (2 or 4) appears randomly
        """
        if depth == 0 or not (self.move()):
            return self.score

        elif node == "max":
            grid, zeros, score = copy(self.grid, self.zero, self.score)
            tps = -100000
            # for move in self.all_moves:
            for key in self.actionkeys:
                if self.action(key, rd=False):
                    comparaison = int(tps)
                    tps = max(tps, self.alphabeta(depth - 1, alpha, beta, "min"))
                    if depth == self.depth and comparaison != tps:
                        self.real_move = key
                    if tps >= beta:
                        return tps
                    alpha = max(alpha, tps)
                self.grid, self.zero, self.score = copy(grid, zeros, score)

        elif node == "min":
            grid, zeros, score = copy(self.grid, self.zero, self.score)
            tps = 100000
            for x in zeros:
                for y in [2, 4]:
                    self.grid[x] = y
                    self -= x
                    tps = min(tps, self.alphabeta(depth - 1, alpha, beta, "max"))
                    if alpha >= tps:
                        return tps
                    beta = min(beta, tps)
                    self.grid, self.zero, self.score = copy(grid, zeros, score)

        return tps

    def expectiminimax(self, depth: int, chance: int = 0, node: str = "max") -> int:
        """
        Function expectiminimax:
        | Maximize the score with weights to force movements so that the game shapes
        | as a zigzag while minimizing the losses when a number (2 or 4) appears randomly
        """
        if depth == 0 or not (self.move()):
            return sum((x * y for x, y in zip(self.WEIGHTS, self.grid)))

        elif node == "max":
            grid, zeros, score = copy(self.grid, self.zero, self.score)
            maxi = -(10 ** 100)
            # for move in self.all_moves:
            for key in self.actionkeys:
                if self.action(key, rd=False):
                    tps = self.expectiminimax(depth - 1, node="chance")
                    if tps > maxi:
                        maxi = tps
                        if depth == self.depth:
                            self.real_move = key
                    self.grid, self.zero = copy(grid, zeros)
            return maxi

        elif node == "min":
            grid, zeros, score = copy(self.grid, self.zero, self.score)
            mini = 10 ** 100
            for y in (2, 4):
                self.grid[chance] = y
                self -= chance
                tps = self.expectiminimax(depth - 1, node="max")
                if tps < mini:
                    mini = tps
                self.grid, self.zero = copy(grid, zeros)
            return mini

        elif node == "chance":
            zeros = copy(self.zero)
            average = [self.expectiminimax(depth, c, node="min") for c in zeros]
            return sum(average) / len(average)


if __name__ == "__main__":
    ai = DecisionAI()
    ai.start(depth=4, solver="minimax")
