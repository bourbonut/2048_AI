from artneunets import *
from random import choice, randint
import matplotlib.pyplot as plt
from copy import copy
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class GeneticAlgorithm(Population):

    """
    Toutes les IAs subissent un traitement:
     - croisement
     - mutation
    """

    def __init__(
        self, params_generation: dict, params_population: dict, params_ai: dict
    ) -> None:
        # Initialisation de la population, du nombre de generations etc...
        Population.__init__(self, params_population, params_ai)
        self.params = params_generation
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

    def selection(self) -> None:
        meanscore = sum(self.scores) / len(self.scores)
        self.mean_scores.append(meanscore)

        # Sélectionne les meilleures IAs
        copie = copy(self.scores)
        copie.sort(reverse=True)
        final = copie[: int(self.params["portion"] * self.length)]
        self.best_ais = [self.scores.index(f) for f in final]

        # Sélectionne les IAs à croiser
        copie = copy(self.scores)
        for i in self.best_ais:
            copie.remove(self.scores[i])
        for _ in range(len(copie) // 2):
            x = choice(copie)
            self.childs.append(self.scores.index(x))
            copie.remove(x)

        # Selectionne les IAs à mutater
        self.mutated = [self.scores.index(copie[i]) for i in range(len(copie))]

    def croisement(self) -> list:
        # Mise en place de la liste des childs et des parents
        childs = [self[i] for i in self.childs]
        parents = [self[i] for i in self.best_ais]
        taille_parents = len(parents)

        for i in range(len(childs)):
            # Nombre des parents transmettant leurs genes
            nombre_parents = randint(1, taille_parents)
            next_parents = []
            index_parents = list(range(len(parents)))

            # Liste des parents transmettant leurs genes
            for _ in range(nombre_parents):
                x = choice(index_parents)
                next_parents.append(x)
                index_parents.remove(x)

            # Initialisation des weights de childs
            weights = childs[i].weights

            # Calcul de nouveaux weights
            for p, w in zip(next_parents, range(self.n_weights)):
                weights[w] += parents[p][w]

            # Mise à jour des weights de childs
            for w in range(self.n_weights):
                childs[i][w] = weights[w] / (len(next_parents) + 1)

        return childs

    def mutation(self) -> list:
        # Mise en place des listes des IAs à muter et des géniteurs
        mutated = [self[i] for i in self.mutated]
        genes_donors = [self[i] for i in self.best_ais]

        nb_genes = []
        for shape in self.shapes:
            nb_genes.append(int(shape[0] * shape[1] * self.params["rd"] * 0.5))

        for i in range(len(mutated)):
            # Choix aléatoire du géniteur
            index_gen = randint(0, len(genes_donors) - 1)
            gen = genes_donors[index_gen]

            for w in range(len(nb_genes)):
                # Mutation des weights
                for _ in range(nb_genes[w]):
                    shape = self.shapes[w]
                    x, y = randint(0, shape[0] - 1), randint(0, shape[1] - 1)
                    mutated[i][w][x, y] = gen[w][x, y]

        return mutated

    def next_generation(self) -> None:
        self.selection()

        liste_best = [copy(self[index]) for index in self.best_ais]

        # Ajout de la meilleure IA de la génération à la liste des meilleures IAs
        self.best_scores.append(liste_best[0].score)
        # Sauvegarde de la meilleure IA de toutes les générations
        if liste_best[0].score > self.ultimate_ai.score:
            self.ultimate_ai = copy(liste_best[0])
        # Croisement
        liste_croisement = self.croisement()
        # Mutation
        liste_mutated = self.mutation()
        # Mise en place de la nouvelle génération
        self.set_population(liste_best + liste_croisement + liste_mutated)

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
