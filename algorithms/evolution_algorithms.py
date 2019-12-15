from algorithms import algorithm
import numpy as np
import random
from tkinter import messagebox


def get_all_algorithms(core):#to be improved
    '''returns dictionary with all algorithms'''
    algo_list = [EvolutionOne(core)]
    algo_dict = {}
    for algo in algo_list:
        algo_dict[algo.get_name()] = algo
    
    return algo_dict

class EvolutionAlgorithm(algorithm.Algorithm):

    def __init__(self,core):
        super().__init__()
        self.core = core

    def build_next_gen(self):
        raise NotImplementedError

class EvolutionOne(EvolutionAlgorithm):

    def build_next_gen(self,generation):
        fitnesses = [shape.fittness for shape in generation]
        fitness_sum = sum(fitnesses)
        normalized_fittness = [fitness/fitness_sum for fitness in fitnesses]
        print(normalized_fittness)
        
        next_generation = []

        for _ in range(len(generation)-1):
            try:
                shape1 = np.random.choice(generation, p=normalized_fittness)
                shape2 = np.random.choice(generation, p=normalized_fittness)
            except ValueError as e:
                messagebox.showerror('error', e)
                raise
            pairing_algorithm = random.choice([algorithm for algorithm in self.core.pairing_algorithms if algorithm.activated])
            new_shape = pairing_algorithm.pair_shapes(shape1,shape2)
            next_generation.append(new_shape)
        next_generation.append(np.random.choice(generation, p=normalized_fittness))
        return next_generation

    def get_name(self):
        return 'Evolution One'

    def default_settings(self):
        pass