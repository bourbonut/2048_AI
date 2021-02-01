# 2048 Intelligence artificielle

## Description

Le but de ce projet est de créer un intelligence artificielle sur le jeu 2048

## Choix du langage de programmation

J'ai choisi d'utiliser le langage de programmation Python pour les raisons suivantes:
- Lorsque j'ai eu l'idée de ce projet, j'avais besoin d'un langage rapide à apprendre, facile à utiliser. Il se trouve qu'en classe préparatoire, Python est le langage qui est enseigné. 
- Python est connu pour sa simplicité. Il est souvent utilisé dans des projets de Machine Learning (bien que ce projet n'utilise pas de base de données).
- La communauté autour du langage Python est développée. Avoir accès à des packages comme pygame, scipy, numpy par exemple est un plus.

## Les différents algorithmes utilisés

Deux versions différentes d'algorithmes génétiques accompagnées de réseaux de neurones:

- `genetic_algorithm_1.py` : dans cet algorithme, la première génération comporte des intelligences artificielles (ias) avec des réseaux de neurones aléatoires. Une fois qu'elles ont joué, je sélectionne les meilleures ias. La nouvelle génération est créée à partir de 3 groupes: un groupe avec les meilleures ias, un groupe avec des ias aléatoires croisées avec les meilleures ias et un groupe avec les meilleures ias avec des gênes mutés. Toutes les ias (qui ne sont pas les meilleures ias) subissent ou bien un croisement, ou bien une mutation.
- `genetic_algorithm_2.py`: cet algorithme utilise le même principe que le premier, mais parmi toutes les ias à croiser ou à muter, certaines ne seront ni croiser ni muter.

Dans le fichier `decisions_algorithms.py`:

- algorithme minimax
- algorithme alphabeta : plus optimisé que minimax
- algorithme expectiminimax : plus performant que minimax

## Résultats

Les algorithmes génétiques ont une convergence très lente. Plus de tests devraient être effectués pour trouver une configuration optimale.
Les algorithmes de décision sont très performants. Le meilleur étant expectiminimax. Un dernier algorithme serait de faire évoluer le paramètre depth en fonction de la difficulté.

## Notes complémentaires

La fonction `backpropagation` du fichier `neural_networks.py` dans `artneunets` n'est pas utilisée dans le reste du projet. Je l'ai créé au départ pour avoir un réseau de neurones opérationnel. Mais dans mes idées d'intelligence artificielle, je n'ai pas eu recours à cette fonction.
