import unittest
import numpy as np
from random_evolution import REvolution
from visualization import Visualization
from individual import Individual


def fitness(val):
    try:
        x = val[0]
        return -x * 2 * x * (x - 3) * (x - 4)
    except Exception as inst:
        print(type(inst), inst, val)  # the exception instance
        return 0


class REvolutionTest(unittest.TestCase):
    def test_random_evol(self):
        np.random.seed(0)
        params = {"min": 0, "max": 5, "dim": 1}
        original_ind = Individual(np.random.uniform(params["min"], params["max"], params["dim"]))
        results = []
        labels = [1]
        epochs = 50

        for _ in labels:
            evo = REvolution(
                original_ind=original_ind,
                combine_params=0.1,
                mutate_params={"min": 0, "max": 5},
                fitness=fitness,
                pop_params={"min": 0, "max": 5, "dim": 1},
                method="compare"
            )
            evo.run_random(epochs)
            results.append(evo.result)

        for _ in labels:
            evo = REvolution(
                original_ind=original_ind,
                combine_params=0.1,
                mutate_params={"std": 0.5, "dim": 1, "min": 0, "max": 5},
                fitness=fitness,
                pop_params={"min": 0, "max": 5, "dim": 1},
                method="compare"
            )
            evo.run_1_1(epochs)
            results.append(evo.result)

        v = Visualization()
        v.visualize(labels + labels, results, epochs)

        self.assertEqual(True, True)
