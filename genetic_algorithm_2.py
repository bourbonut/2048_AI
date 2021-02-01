from artneunets import *
from random import choice, randint, uniform, random
import matplotlib.pyplot as plt
from copy import copy
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class GeneticAlgorithm(Population):

    """
    Une partie des IAs subissent un traitement:
     - croisement
     - mutation

    L'autre partie des Ias est non mutee
    """

    def __init__(
        self, params_generation: dict, params_population: dict, params_ai: dict
    ) -> None:
        # Initialisation de la population, du nombre de générations etc...
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
        Permet de faire évoluer la population et
        d'afficher le score de la meilleure IA par génération
        """
        generations = []
        # Début du graphe dynamique
        plt.ion()
        for i in range(self.params["n_generation"]):
            self.play()
            self.next_generation()
            generations.append(i)
            plt.plot(generations, self.best_scores)
            plt.plot(generations, self.mean_scores)
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
        # Mise à zéro des listes suivantes
        meanscore = sum(self.scores) / len(self.scores)
        self.mean_scores.append(meanscore)

        # Sélectionne les meilleures IAs
        copie = copy(self.scores)
        copie.sort(reverse=True)
        final = copie[: int(self.params["portion"] * self.length)]
        self.best_ais = [self.scores.index(f) for f in final]

    def croisement(self) -> list:
        crossover = []
        for _ in range(int(self.length - 2 * len(self.best_ais) / 2)):
            # Par couple de parents,
            # Initialisation des parents
            parent1 = self[choice(self.best_ais)]
            parent2 = self[choice(self.best_ais)]
            # Initialisation des enfants
            child1 = ArtInt(self.params_ai)
            child2 = ArtInt(self.params_ai)

            # Pour child1, moyenne des weights des parents
            for w in range(self.n_weights):
                child1[w] = (parent1[w] + parent2[w]) / 2

            self.weight_per_weight(child2, parent2, parent1)
            crossover.append(child1)
            crossover.append(child2)

        return crossover

    def mutation(self, liste_best: list) -> None:
        # Copie des meilleures IAs à muter
        self.mutated = [copy(ai) for ai in liste_best]
        # Parcoure toutes les Ias à muter
        for i in range(len(self.mutated)):
            # Pourcentage de mutations
            nb_genes = [int(s[0] * s[1] * self.params["rd"]) for s in self.shapes]

            for w in range(len(nb_genes)):
                for _ in range(nb_genes[w]):
                    shape = self.shapes[w]
                    x, y = randint(0, shape[0] - 1), randint(0, shape[1] - 1)
                    value = self.mutated[i][w][x, y] + 5 * random() - 2.5
                    self.mutated[i][w][x, y] = value

    def next_generation(self) -> None:
        self.selection()

        liste_best = [copy(self[index]) for index in self.best_ais]

        # Ajout de la meilleure IA de la génération à la liste des meilleures IAs
        self.best_scores.append(liste_best[0].score)
        # Sauvegarde de la meilleure IA de toutes les générations
        if liste_best[0].score > self.ultimate_ai.score:
            self.ultimate_ai = copy(liste_best[0])

        # Mutation
        self.mutation(liste_best)
        # Croisement
        liste_best.extend(self.croisement())
        # Mise à jour avec la liste des IAs mutees
        liste_best.extend(self.mutated)
        # Mise en place de la nouvelle génération
        self.set_population(liste_best)

    def best(self) -> None:
        """Affiche la meilleure IA"""
        self.ultimate_ai.start()
        print(self.ultimate_ai.score)


if __name__ == "__main__":
    config = yaml.load(stream=open("config.yaml", "r"), Loader=Loader)

    params_generation = config["params_generation"]
    params_population = config["params_population"]
    params_ai = config["params_ai"]

    a = GeneticAlgorithm(params_generation, params_population, params_ai)
    a.evolve()
