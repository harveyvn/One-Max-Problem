from population import Population


class REvolution:
    def __init__(self, original_ind, combine_params, mutate_params, fitness, pop_params, method):
        self.population = Population(1, fitness, pop_params)
        self.combine_params = combine_params
        self.mutate_params = mutate_params
        self.fitness = fitness
        self.method = method
        self.result = []
        self.original_ind = original_ind

    def run_random(self, epochs):
        for ep in range(epochs):
            pop_ind = self.population.individuals[0]
            offspring = pop_ind.compare(self.original_ind, self.combine_params, self.fitness)
            offspring.mutate_random(self.mutate_params)
            self.population.arrange_population([offspring])
            print("Epoch {}: {}".format(ep, self.get_pop()))
            self.result.append(self.fitness(self.population.individuals[-1].value))

    def run_1_1(self, epochs):
        for ep in range(epochs):
            pop_ind = self.population.individuals[0]
            offspring = pop_ind.compare(self.original_ind, self.combine_params, self.fitness)
            offspring.mutate(self.mutate_params)
            self.population.arrange_population([offspring])
            print("Epoch {}: {}".format(ep, self.get_pop()))
            self.result.append(self.fitness(self.population.individuals[-1].value))

    def get_pop(self):
        ids = ["x: {} => y: {}".format("%.3f" % i.value[0], "%.3f" % self.fitness(i.value))
               for i in self.population.individuals]
        return ids
