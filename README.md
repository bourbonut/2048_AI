# 2048 Artificial intelligence

## Description

What ?
> The goal is to make an artificial intelligence on the game 2048.

Why ?
> Because it's fun.
> 
How ?
> For the moment, there are only few algorithms written:
- minimax
- alphabeta
- expectiminimax
- 2 different genetic algorithms

## Choice of the programming language

Obviously Python because it's easy to learn, to read, to debug.
In addition, I'm using:
- `pygame` to manage the 2D graphic interface of the game.
- `numpy` to manage array calculations in the neural networks
- `matplotlib` to draw and show graphs

There are easy to use.

## Algorithms

Two different versions of genetic algorithms (file `genetic_algorithms.py`):

- `GeneticAlgorithm1`: The first generation is composed of artificial intelligences (A.I.) with random neural networks weights. After they have played, best A.I are selected. A new generation is created depending on 3 groups: a group with the best A.I., a group with A.I. randomly crossed with the best A.I. and a group with the best A.I. but some of their genes are mutated. All A.I. are either crossed either mutated
- `genetic_algorithm_2.py`: it almost the same but among all A.I. to cross or to mutate, some ones won't be neither crossed neither mutated.

In the file `decisions_algorithms.py`:

- algorithm minimax
- algorithm alphabeta : more optimized than minimax
- algorithm expectiminimax : more efficient than minimax

## Results

The convergence of genetic algorithms are slow. More tests must be done to get a better configuration.
Decision algorithms are efficient. The best one is expectiminimax.
