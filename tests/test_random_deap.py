import unittest
import numpy as np
from individual import Individual
from deap_evolution import DeapEvolution

FIRST = 0


def fitness(deap_inds):
    individual = deap_inds[FIRST]  # deap_individual is a list
    try:
        x = individual.value[0]
        return -x * 2 * x * (x - 3) * (x - 4),
    except Exception as inst:
        print(type(inst), inst, individual)  # the exception instance
        return 0,


def expectations(gens):
    x = 3.569
    return [-x * 2 * x * (x - 3) * (x - 4) for _ in range(gens)]


def generate_random_ind():
    params = {"min": 0, "max": 5, "dim": 1}
    return Individual(np.random.uniform(params["min"], params["max"], params["dim"]))


def mutate(deap_inds, mutate_params):
    individual = deap_inds[FIRST]  # deap_individual is a list

    value = individual.value  # extract attribute value from an individual
    std, dim = mutate_params['std'], mutate_params['dim']
    value += np.random.normal(0, std, dim)
    if value <= mutate_params['min']:
        value[0] = mutate_params['min']
    if value >= mutate_params['max']:
        value[0] = mutate_params['max']

    individual.value = value
    return individual  # return deap_individual


def select(orig_ind, pop_ind, fitness):
    deap_inds = pop_ind[FIRST]  # deap_pop is a list
    target_ind = deap_inds[FIRST]  # deap_individual is a list

    if fitness([orig_ind]) >= fitness([target_ind]):
        value = orig_ind.value
        fitness_value = fitness([orig_ind])
    else:
        value = target_ind.value
        fitness_value = deap_inds.fitness.values

    deap_inds.fitness.values = fitness_value  # update fitness value to offspring
    deap_inds[FIRST].value = value  # update attribute value to offspring
    return deap_inds  # return deap_individual


class DeapRandomTest(unittest.TestCase):
    def test_deap_evolution(self):
        self.assertEqual(0, 0)
        rEv = DeapEvolution(fitness, mutate, select, generate_random_ind, expectations)

        np.random.seed(64)
        params = {"min": 0, "max": 5, "dim": 1}
        original_ind = Individual(np.random.uniform(params["min"], params["max"], params["dim"]))

        rEv.start_from(original_ind, 1)

        rEv.print_logbook()
        rEv.visualize_evolution()

