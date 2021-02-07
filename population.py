import numpy as np
from individual import Individual


class Population:
    def __init__(self, size, fitness, params):
        self.fitness = fitness
        self.individuals = [Individual(np.random.uniform(params["min"], params["max"], params["dim"]))
                            for _ in range(size)]
        self.size = size

    def arrange_population(self, offsprings):
        # calculate fitness offspring
        self.individuals = self.individuals + offsprings
        self.individuals = sorted(self.individuals, key=lambda x: self.fitness(x.value), reverse=False)
        # let the weakness die
        self.individuals = self.individuals[-self.size:]


    def get_pairs(self):
        odds = self.individuals[1::2]
        evens = self.individuals[0::2]
        return odds, evens
