import unittest
import numpy as np
from copy import deepcopy
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


def generate_random_ind(original_ind):
    params = {"min": 0, "max": 5, "dim": 1}
    random_ind = deepcopy(original_ind)
    random_ind.value = np.random.uniform(params["min"], params["max"], params["dim"])
    return random_ind


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


def select(orig_ind, pop_ind):
    deap_inds = pop_ind[FIRST]  # deap_pop is a list
    target_ind = deap_inds[FIRST]  # deap_individual is a list

    f1 = orig_ind.fitness.values
    f2 = deap_inds.fitness.values

    if f1 >= f2:
        value = orig_ind[FIRST].value
        fitness_value = f1
    else:
        value = target_ind.value
        fitness_value = f2

    deap_inds.fitness.values = fitness_value  # update fitness value to offspring
    deap_inds[FIRST].value = value  # update attribute value to offspring
    return deap_inds  # return deap_individual


class DeapRandomTest(unittest.TestCase):
    def test_deap_evolution(self):
        self.assertEqual(0, 0)

        np.random.seed(64)
        params = {"min": 0, "max": 5, "dim": 1}
        original_ind = Individual(np.random.uniform(params["min"], params["max"], params["dim"]))

        rEv = DeapEvolution(
            original_ind=original_ind,
            fitness=fitness,
            select=select,
            generate_random_ind=generate_random_ind,
            expectations=expectations
        )
        rEv.start_from(0.0025)

        rEv.print_logbook()
        rEv.visualize_evolution()

