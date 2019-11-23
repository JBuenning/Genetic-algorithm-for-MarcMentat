import shape
import GUI
import examples
import mentat_connection

class Core:
    def __init__(self):
        self.generations = [] #list with all generations, generation[0] is the inital generation
        self.inital_shape = None #Shape that the user wants to improve
        self.mutation_algorithms = []

        ### Test - soll später noch verändert werden ###
        self.inital_shape = examples.get_realisticreate_example_polygonc_example()

    def generate_first_generation(self): #fills the first array of self.generations with random shapes
        self.generations = []
        pass
    
    def get_random_shape(self,algorithm):
