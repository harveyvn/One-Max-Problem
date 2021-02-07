from evolution import Evolution
from visualization import Visualization


def fitness(val):
    try:
        x = val[0]
        return -x * 2 * x * (x - 3) * (x - 4)
    except Exception as inst:
        print(type(inst), inst, val)  # the exception instance
        return 0


if __name__ == '__main__':
    results = []
    labels = [4, 6, 8, 10]
    epochs = 60
    for i in labels:
        evo = Evolution(
            size=i,
            fitness=fitness,
            combine_params=0.5,
            mutate_params={"std": 0.5, "dim": 1, "min": 0, "max": 5},
            pop_params={"min": 0, "max": 5, "dim": 1},
            method="combine"
        )
        evo.run(epochs)
        results.append(evo.result)
    for i in labels:
        evo = Evolution(
            size=i,
            fitness=fitness,
            combine_params=0.1,
            mutate_params={"std": 0.5, "dim": 1, "min": 0, "max": 5},
            pop_params={"min": 0, "max": 5, "dim": 1},
            method="compare"
        )
        evo.run(epochs)
        results.append(evo.result)

    v = Visualization()
    v.visualize(labels + labels, results, epochs)
