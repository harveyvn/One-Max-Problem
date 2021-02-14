import unittest
import numpy as np
import matplotlib.pyplot as plt
from individual import Individual
from deap import tools, creator, base

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


def random_ind():
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
    def test_deap_random(self):
        self.assertEqual(0, 0)
        np.random.seed(64)
        params = {"min": 0, "max": 5, "dim": 1}
        original_ind = Individual(np.random.uniform(params["min"], params["max"], params["dim"]))

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        # Attribute generator
        toolbox.register("attr_val", random_ind)
        # Structure initializers
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_val, 1)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", fitness)
        toolbox.register("mutate", mutate, mutate_params={"std": 0.25, "dim": 1, "min": 0, "max": 5})
        toolbox.register("select", select, fitness=fitness)

        stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(key=len)
        mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        mstats.register("avg", np.mean)
        mstats.register("std", np.std)
        mstats.register("min", np.min)
        mstats.register("max", np.max)
        logbook = tools.Logbook()

        pop = toolbox.population(n=1)
        print("Start of evolution")

        # Evaluate the entire population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        print("  Evaluated %i individuals" % len(pop))

        # Extracting all the fitnesses of
        fits = [ind.fitness.values[0] for ind in pop]
        g = 0
        gs = 100

        # Begin the evolution
        while g < gs:
            # A new generation
            g = g + 1
            # Select the next generation individuals
            offspring = toolbox.select(original_ind, pop)
            toolbox.mutate(offspring)
            # The population is entirely replaced by the offspring
            pop[:] = [offspring]
            best_ind = tools.selBest(pop, 1)[0]
            record = mstats.compile(pop)
            logbook.record(gen=g, evals=gs, **record)

        logbook.header = "gen", "evals", "fitness", "size"
        logbook.chapters["fitness"].header = "min", "avg", "max"
        logbook.chapters["size"].header = "min", "avg", "max"
        print(logbook)

        gen = logbook.select("gen")
        fit_mins = logbook.chapters["fitness"].select("min")
        size_avgs = logbook.chapters["size"].select("avg")

        fig, ax1 = plt.subplots()
        line1 = ax1.plot(gen, fit_mins, "b-", label="Fitness")
        line3 = ax1.plot(gen, expectations(gs), "b--", label="Expectation")
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Fitness", color="b")
        for tl in ax1.get_yticklabels():
            tl.set_color("b")

        ax2 = ax1.twinx()
        line2 = ax2.plot(gen, size_avgs, "r-", label="Size")
        ax2.set_ylabel("Size", color="r")
        for tl in ax2.get_yticklabels():
            tl.set_color("r")

        lns = line1 + line2 + line3
        # lns = line1
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc="lower right")

        plt.show()
