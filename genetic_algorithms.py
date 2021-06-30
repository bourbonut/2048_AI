from artneunets import *
from random import choice, randint, uniform, random
from copy import copy
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class GeneticAlgorithm1(GeneticPattern):

    """
    All A.I. have the same treatement:
     - crossover
     - mutation
    """

    def selection(self) -> None:
        self.mean_scores.append(sum(self.scores) / len(self.scores))

        # Select the best A.I.
        scores = copy(self.scores)
        scores.sort(reverse=True)
        final = scores[: int(self.params["portion"] * self.length)]
        self.best_ais = [self.scores.index(f) for f in final]

        # Select A.I. to cross
        scores = copy(self.scores)
        for i in self.best_ais:
            scores.remove(self.scores[i])
        self.childs = []
        for _ in range(len(scores) // 2):
            x = choice(scores)
            self.childs.append(self.scores.index(x))
            scores.remove(x)

        # Select A.I. to mutate
        self.mutated = [self.scores.index(scores[i]) for i in range(len(scores))]

    def crossover(self) -> list:
        # Setting up the child list and the parent list
        childs = [self[i] for i in self.childs]
        parents = [self[i] for i in self.best_ais]
        size_parents = len(parents)

        for i in range(len(childs)):
            # Number of parents giving their genes
            number_parents = randint(1, size_parents)
            next_parents = []
            index_parents = list(range(len(parents)))

            # List of parents giving their genes
            for _ in range(number_parents):
                x = choice(index_parents)
                next_parents.append(x)
                index_parents.remove(x)

            # Initialization of weights of childs
            weights = childs[i].weights

            # Calculation of new weights
            for p, w in zip(next_parents, range(self.n_weights)):
                weights[w] += parents[p][w]

            # Setting up the weights of childs
            for w in range(self.n_weights):
                childs[i][w] = weights[w] / (len(next_parents) + 1)

        return childs

    def mutation(self) -> list:
        # Setting up A.I. list for mutation and their gene donors
        mutated = [self[i] for i in self.mutated]
        gene_donors = [self[i] for i in self.best_ais]

        nb_gene = []
        for shape in self.shapes:
            nb_gene.append(int(shape[0] * shape[1] * self.params["rd"] * 0.5))

        for i in range(len(mutated)):
            # Random choice of gene donor
            index_gen = randint(0, len(gene_donors) - 1)
            gene = gene_donors[index_gen]

            for w in range(len(nb_gene)):
                # Mutation of weights
                for _ in range(nb_gene[w]):
                    shape = self.shapes[w]
                    x, y = randint(0, shape[0] - 1), randint(0, shape[1] - 1)
                    mutated[i][w][x, y] = gene[w][x, y]

        return mutated


class GeneticAlgorithm2(GeneticPattern):

    """
    A part of A.I. has the following treatement:
     - crossover
     - mutation

    The other part of A.I. is not mutated.
    """

    def weight_per_weight(self, child: list, parent1: list, parent2: list) -> None:
        if parent1.score < parent2.score:
            parent1, parent2 = parent2, parent1
        for w, shape in enumerate(self.shapes):
            for x in range(shape[0]):
                for y in range(shape[1]):
                    if random() >= 0.5:
                        child[w][x, y] = parent1[w][x, y]
                    else:
                        child[w][x, y] = parent2[w][x, y]

    def selection(self) -> None:
        self.mean_scores.append(sum(self.scores) / len(self.scores))

        # Select the best A.I.
        scores = copy(self.scores)
        scores.sort(reverse=True)
        final = scores[: int(self.params["portion"] * self.length)]
        self.best_ais = [self.scores.index(f) for f in final]
        self.mutated = [copy(self[index]) for index in self.best_ais]

    def crossover(self) -> list:
        crossover = []
        for _ in range(int(self.length - 2 * len(self.best_ais) / 2)):
            # By pair of parents,
            # Setting up parents
            parent1 = self[choice(self.best_ais)]
            parent2 = self[choice(self.best_ais)]
            # Setting up childs
            child1 = ArtInt(self.params_ai)
            child2 = ArtInt(self.params_ai)

            # For child1, mean of weights of parents
            for w in range(self.n_weights):
                child1[w] = (parent1[w] + parent2[w]) / 2

            # For child2, random genes of parent1 et parent2
            self.weight_per_weight(child2, parent2, parent1)
            crossover.append(child1)
            crossover.append(child2)

        return crossover

    def mutation(self) -> None:
        mutation = self.mutated
        for i in range(len(mutation)):
            # Percentage of mutation
            nb_genes = [int(s[0] * s[1] * self.params["rd"]) for s in self.shapes]

            for w in range(len(nb_genes)):
                for _ in range(nb_genes[w]):
                    shape = self.shapes[w]
                    x, y = randint(0, shape[0] - 1), randint(0, shape[1] - 1)
                    value = mutation[i][w][x, y] + 5 * random() - 2.5
                    mutation[i][w][x, y] = value
        return mutation


if __name__ == "__main__":
    config = yaml.load(stream=open("config.yaml", "r"), Loader=Loader)

    params_generation = config["params_generation"]
    params_population = config["params_population"]
    params_ai = config["params_ai"]

    algo = GeneticAlgorithm1(params_generation, params_population, params_ai)
    algo.evolve()
