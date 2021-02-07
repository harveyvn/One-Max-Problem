import numpy as np
from abc import ABC, abstractmethod


class IndividualBase(ABC):
    def __init__(self, value=None):
        self.value = value

    @abstractmethod
    def combine(self, father, combine_params):
        pass

    @abstractmethod
    def compare(self, father, combine_params, fitness):
        pass

    @abstractmethod
    def mutate(self, mutate_params):
        pass

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Individual(IndividualBase):
    def combine(self, father, combine_params):
        value = self.value * combine_params + father.value * combine_params
        return Individual(value)

    def compare(self, father, combine_params, fitness):
        if fitness(self.value) >= fitness(father.value):
            value = self.value + self.value * combine_params
        else:
            value = father.value + father.value * combine_params
        return Individual(value)

    def mutate(self, mutate_params):
        std, dim = mutate_params['std'], mutate_params['dim']
        self.value += np.random.normal(0, std, dim)
        if self.value[0] < mutate_params['min']:
            self.value[0] = mutate_params['min']
        if self.value[0] > mutate_params['max']:
            self.value[0] = mutate_params['max']
