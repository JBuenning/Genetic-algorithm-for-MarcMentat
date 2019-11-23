import shape
import examples
import mentat_connection
import random
from algorithms import mutation_algorithms
from tkinter import messagebox


class Core:
    def __init__(self):
        self.generations = [] #list with all generations, generation[0] is the inital generation
        self.inital_shape = None #Shape that the user wants to improve
        self.mutation_algorithms = mutation_algorithms.get_all_mutation_algorithms()
        self.mentat_connections = []
        self.mentat_commands = []

        self.default_settings()

    def generate_first_generation(self): #fills the first array of self.generations with random shapes
        self.generations = []
        generation = []
        if not self.inital_shape:
            messagebox.showerror('error', 'no initial shape')
        elif not self.mutation_algorithms:
            messagebox.showerror('error', 'no mutation algorithm selected')
        else:
            for _ in range(self.first_generation_size):
                algorithm = random.choice(self.mutation_algorithms)
                shp = algorithm.change_shape(self.inital_shape)
                generation.append(shp)
            self.generations.append(generation)

    def default_settings(self):
        self.first_generation_size = 60
    
    def mutate_shape(self,algorithm):
        pass

    def evaluate_shapes(self, shapes):
        return []