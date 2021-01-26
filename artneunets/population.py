from artneunets.ai import ArtInt
import threading
import time


class Population:

    """Classe Population qui est un groupe d'intelligences artificielles (classe ArtInt)"""

    def __init__(self, params_population, params_ai):
        # Création d'une population d'IA
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
        """Fait jouer les IAs a tour de role"""
        for i, ai in enumerate(self.ais):
            ai.ai_start(function)
            self.scores[i] = ai.score

    def thread_run(self, function: callable) -> None:
        """Fait jouer les IAs en meme temps avec des threads"""
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
        """Permet de recuperer la moyenne des scores des differents jeux"""
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
