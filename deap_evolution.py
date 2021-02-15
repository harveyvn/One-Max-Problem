import numpy as np
import matplotlib.pyplot as plt
from deap import tools, creator, base
from threading import Thread, Event

# Event object used to send signals from one thread to another
stop_event = Event()
FIRST = 0


class DeapEvolution:
    def __init__(self, original_ind, fitness, select, generate_random_ind, expectations):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()
        # Attribute generator
        self.toolbox.register("random_ind", generate_random_ind, original_ind)
        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.random_ind, 1)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", fitness)
        self.toolbox.register("select", select)

        stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(key=len)
        self.mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        self.mstats.register("avg", np.mean)
        self.mstats.register("std", np.std)
        self.mstats.register("min", np.min)
        self.mstats.register("max", np.max)
        self.logbook = tools.Logbook()

        self.expectations = expectations

    def start_from(self, timeout):
        def _run():
            pop = self.toolbox.population(n=1)
            print("Start of evolution")

            # Evaluate the entire population
            fitnesses = list(map(self.toolbox.evaluate, pop))
            for ind, fit in zip(pop, fitnesses):
                ind.fitness.values = fit

            best_ind = tools.selBest(pop, 1)[FIRST]
            epochs = 0
            # Begin the evolution
            while True:
                epochs = epochs + 1
                # A new generation
                pop = self.toolbox.population(n=1)
                # Evaluate the entire population
                fitnesses = list(map(self.toolbox.evaluate, pop))
                for ind, fit in zip(pop, fitnesses):
                    ind.fitness.values = fit

                # Select the next generation individuals
                best_ind = self.toolbox.select(best_ind, pop)
                record = self.mstats.compile(pop)
                self.logbook.record(gen=epochs, evals=epochs, **record)
                if stop_event.is_set():
                    break

        # Start the thread evolution within given time
        action_thread = Thread(target=_run)
        action_thread.start()
        action_thread.join(timeout=timeout)
        stop_event.set()

        print("End of evolution")

    def print_logbook(self):
        self.logbook.header = "gen", "evals", "fitness", "size"
        self.logbook.chapters["fitness"].header = "min", "avg", "max"
        self.logbook.chapters["size"].header = "min", "avg", "max"
        print(self.logbook)

    def visualize_evolution(self):
        gen = self.logbook.select("gen")
        fit_mins = self.logbook.chapters["fitness"].select("min")
        size_avgs = self.logbook.chapters["size"].select("avg")

        fig, ax1 = plt.subplots()
        line1 = ax1.plot(gen, fit_mins, "b-", label="Fitness")
        line3 = ax1.plot(gen, self.expectations(len(gen)), "b--", label="Expectation")
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
