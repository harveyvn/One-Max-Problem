from evolution import Evolution


def fitness(val):
    try:
        x = val[0]
        return -x * 2 * x * (x - 3) * (x - 4)
    except Exception as inst:
        print(type(inst), inst, val)  # the exception instance
        return 0


if __name__ == '__main__':
    evo = Evolution(
        size=10,
        fitness=fitness,
        combine_params=0.5,
        mutate_params={"std": 0.5, "dim": 1, "min": 0, "max": 5},
        pop_params={"min": 0, "max": 5, "dim": 1},
    )

    epochs = 20
    evo.run(epochs)