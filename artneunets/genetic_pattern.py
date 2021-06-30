from .ai import ArtInt
from .population import Population
import matplotlib.pyplot as plt
from copy import copy


class GeneticPattern(Population):

    """
    Genetic pattern class used to avoid repetition between all genetic algorithms
    Only the methods `selection`, `crossover` and `mutation` have to be implemented.
    """

    def __init__(
        self, params_generation: dict, params_population: dict, params_ai: dict
    ) -> None:
        # Initialization of the population, the number of generations etc...
        Population.__init__(self, params_population, params_ai)
        self.params = params_generation
        self.params_ai = params_ai
        self.best_scores = []
        self.mean_scores = []
        self.ultimate_ai = copy(self[0])

        sample_weights = self.ultimate_ai.weights
        self.n_weights = len(sample_weights)
        self.shapes = [weight.shape for weight in sample_weights]

    def evolve(self) -> None:
        """
        Function that makes the population evolve and
        display the score of the best A.I. per generation
        """
        generations = []
        plt.ion()
        for i in range(self.params["n_generation"]):
            self.play()
            self.next_generation()
            generations.append(i)
            plt.plot(generations, self.best_scores, label="Best scores")
            plt.plot(generations, self.mean_scores, label="Mean scores")
            plt.xlabel("Generation")
            plt.ylabel("Score")
            plt.draw()
            plt.pause(0.0001)
            plt.clf()
        plt.plot(generations, self.best_scores)
        plt.show()
        input("Press any key to quit.")

    def play(self) -> None:
        self.thread_run(self.params["run_type"])

    def next_generation(self) -> None:
        self.selection()

        list_best = [copy(self[index]) for index in self.best_ais]
        self.best_scores.append(list_best[0].score)

        # Save the best A.I. if it is better than all previous ones
        if list_best[0].score > self.ultimate_ai.score:
            self.ultimate_ai = copy(list_best[0])

        self.set_population(list_best + self.crossover() + self.mutation())

    def best(self) -> None:
        """Let the best A.I. plays and print the score"""
        self.ultimate_ai.start()
        print(self.ultimate_ai.score)
