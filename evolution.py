from population import Population


class Evolution:
    def __init__(self, size, combine_params, mutate_params, fitness, pop_params, method):
        self.population = Population(size, fitness, pop_params)
        self.combine_params = combine_params
        self.mutate_params = mutate_params
        self.fitness = fitness
        self.method = method
        self.result = []

    def run(self, epochs):
        for ep in range(epochs):
            offsprings = []
            odds, evens = self.population.get_pairs()
            for odd, even in zip(odds, evens):
                # produce offspring
                if self.method == "combine":
                    # average of 2 individuals
                    offspring = odd.combine(even, self.combine_params)
                if self.method == "compare":
                    # pick the best individual
                    offspring = odd.compare(even, self.combine_params, self.fitness)
                # mutate offspring
                offspring.mutate(self.mutate_params)
                offsprings.append(offspring)
            self.population.arrange_population(offsprings)
            print("Epoch {}: {}".format(ep, self.get_pop()))
            self.result.append(self.fitness(self.population.individuals[-1].value))

    def get_pop(self):
        ids = ["x: {} => y: {}".format("%.3f" % i.value[0], "%.3f" % self.fitness(i.value))
               for i in self.population.individuals]
        return ids
