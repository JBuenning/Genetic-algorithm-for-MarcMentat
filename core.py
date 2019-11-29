import shape
import examples
import mentat_connection
import random
from algorithms import mutation_algorithms
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor


class Core:
    def __init__(self):
        self.generations = [] #list with all generations, generation[0] is the inital generation
        self.inital_shape = None #Shape that the user wants to improve
        self.mutation_algorithms = mutation_algorithms.get_all_mutation_algorithms()
        self.mentat_connections = []
        #self.mentat_commands = [] #replaced by read_in and evaluation algorighm
        self.read_in_algorithm = None
        self.evaluation_algorithm = None

        self.default_settings()

    def generate_first_generation(self): #fills the first array of self.generations with random shapes
        self.generations = []
        generation = []
        activated_mutation_algorithms = [algo for algo in self.mutation_algorithms if algo.activated]

        if not self.inital_shape:
            messagebox.showerror('error', 'no initial shape')
        elif not activated_mutation_algorithms:
            messagebox.showerror('error', 'no mutation algorithm selected')
        else:
            for _ in range(self.first_generation_size):
                algorithm = random.choice(activated_mutation_algorithms)
                shp = algorithm.change_shape(self.inital_shape)
                generation.append(shp)
            self.generations.append(generation)

    def default_settings(self):
        self.first_generation_size = 60
    
    def mutate_shape(self,algorithm):
        pass

    def evaluate_shapes(self, shapes):#in genera probably better to use a Queue
        def mentat_connection_loop(tasklist, connection):
            task, index = tasklist.get_next_task()
            while not (task is None):
                try:#maybe first try a testobject as the failure of connection might not be detected without timeout(but I am not quite sure)
                    #pickle and send the task
                    #result = wait for result
                    result = None #to be changed!!!!
                    tasklist.return_evaluation(index, True, result)
                except:
                    tasklist.return_evaluation(index, False)
                    break
                task, index = tasklist.get_next_task()


        tasklist = mentat_connection.Tasklist(shapes, self.read_in_algorithm, self.evaluation_algorithm)

        with ThreadPoolExecutor(max_workers=len(self.mentat_connections)) as executor:
            for connection in self.mentat_connections:
                executor.submit(mentat_connection_loop, tasklist, connection)#exceptions might not be visible!!!

        for evaluation in tasklist.evaluations:#test if tasklist was completely evaluated
            if isinstance(evaluation, str):
                print(tasklist.evaluations)
                raise Exception('tasklist not evaluated correctly')

        return tasklist.evaluations
        