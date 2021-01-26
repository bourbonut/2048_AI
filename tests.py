from artneunets import *
import numpy as np
from copy import copy
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

config = yaml.load(stream=open("config.yaml", "r"), Loader=Loader)

params_generation = config["params_generation"]
params_population = config["params_population"]
params_ai = config["params_ai"]


def test_neural_networks():
    """Test 'NeuNets'"""
    neural_networks = NeuNets(params_ai)
    neural_networks.feedforward(
        np.array([8, 2, 16, 0, 0, 2, 4, 2, 4, 16, 0, 4, 2, 0, 0, 0])
    )
    print(neural_networks._output)
    neural_networks.backpropagation(np.array([1, 0, 0, 0]))
    print(neural_networks)


def test_ai():
    """Test 'ArtInt'"""
    a_i_ = ArtInt(params_ai)
    a_i_.ai_start(solver="advanced")
    print(a_i_.score)
    copied_a_i_ = copy(a_i_)
    print("Copie reussie")


def test_population():
    """Test 'Population'"""
    population = Population(params_population, params_ai)
    population.thread_run("basic")
    print(population)


if __name__ == "__main__":
    test_neural_networks()
    test_ai()
    test_population()
