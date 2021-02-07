from population import Population


class Evolution:
    def __init__(self, size, combine_params, mutate_params, fitness, pop_params):
        self.population = Population(size, fitness, pop_params)
        self.combine_params = combine_params
        self.mutate_params = mutate_params
        self.fitness = fitness

    def run(self, epochs):
        for ep in range(epochs):
            offsprings = []
            odds, evens = self.population.get_pairs()
            for odd, even in zip(odds, evens):
                # produce offspring
                offspring = odd.combine(even, self.combine_params)
                # mutate offspring
                offspring.mutate(self.mutate_params)
                offsprings.append(offspring)
            self.population.arrange_population(offsprings)
            print("Epoch {}: {}".format(ep, self.get_pop()))

    def get_pop(self):
        ids = ["x: {} => y: {}".format("%.3f" % i.value[0], "%.3f" % self.fitness(i.value))
               for i in self.population.individuals]
        return ids
