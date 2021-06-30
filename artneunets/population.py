from .ai import ArtInt
import threading
import time


class Population:

    """Population class which is a group of A.I. (ArtInt class)"""

    def __init__(self, params_population, params_ai):
        # Creation of a population of A.I.
        self.length = params_population["length"]
        self.games_played = params_population["games_played"]
        self.ais = [ArtInt(params_ai) for _ in range(self.length)]
        self.scores = [ai.score for ai in self.ais]

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        return self.ais[i]

    def __setitem__(self, key, item):
        self.ais[key] = item

    def __repr__(self):
        disp = f"Population de taille :{self.length}\n"
        disp += "\n".join(map(str, self.ais))
        return disp

    def simple_run(self, function: callable) -> None:
        """Each A.I. plays by turns"""
        for i, ai in enumerate(self.ais):
            ai.ai_start(function)
            self.scores[i] = ai.score

    def thread_run(self, function: callable) -> None:
        """Threads used to have all A.I. playing simultaneously"""
        # Liste des threads
        threads = []
        for i in range(len(self)):
            # Mise en place des threads
            thread = threading.Thread(target=self.multiple_runs, args=(i, function))
            # Lancement des threads
            thread.start()
            threads.append(thread)
        # Permet d'attendre que tous les threads aient termine de jouer
        for i in range(self.length):
            threads[i].join()

    def multiple_runs(self, index: int, function: callable) -> None:
        """Get the mean score back to all different games"""
        meanscore = []
        # Les IAs jouent
        for _ in range(self.games_played):
            self.ais[index].ai_start(function)
            meanscore.append(self.ais[index].score)
        score = sum(meanscore) / len(meanscore)
        self.scores[index] = self.ais[index].score = score

    def append(self, ai):
        self.ais.append(ai)

    def pop(self, index):
        self.ais.pop(index)

    def set_population(self, ais):
        self.ais = ais
