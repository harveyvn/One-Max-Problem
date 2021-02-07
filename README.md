# An Evolutionary Algorithm to solve a simple function maximization problem

## Sample Function:
\[ f(x) = -2x^2(x-3)(x-4) \]

## Concepts:
1. Generate an initial population of individuals randomly.
2. Calculate the fitness score of each individual in the population with a given fitness function.
3. Run the evolution algorithm in the number of iterations:
    * Only select best individuals for producing offsprings.
    * Mutate those offsprings.
    * Merge the offspring to the initial population and evaluate the fitness score of each individual.
    * Remove individuals with a bad fitness score.
4. Select the individual with the highest score as the final solution.

## Questions:
1. What are the individuals?
2. Population size and how to generate the individuals?
3. How to evaluate a fitness score?
4. How to produce and mutate offsprings?
5. How many individuals die?
6. How many epochs will we repeat?
