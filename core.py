import shape
import examples
import mentat_connection
from mentat_connection import HEADERSIZE, Test_connection, Simple_task
import random
from algorithms import mutation_algorithms, read_in_algorithms, evaluation_algorithms, pairing_algorithms
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
#from concurrent.futures import ProcessPoolExecutor as ThreadPoolExecutor
import time
import socket
import pickle
import threading
import numpy as np
import math
import statistics as stat

class Core:
    def __init__(self):
        self.lock = threading.Lock()
        self.optimization_running = False
        self.generations = [] #list with all generations, generation[0] is the inital generation
        self.improvement_history = []
        self.inital_shape = None #Shape that the user wants to improve
        self.mutation_algorithms = mutation_algorithms.get_all_mutation_algorithms()
        self.pairing_algorithms = pairing_algorithms.get_all_pairing_algorithms()
        self.mentat_connections = []
        #self.mentat_commands = [] #replaced by read_in and evaluation algorighm
        self.all_read_in_algorithms = read_in_algorithms.get_all_algorithms()
        if len(self.all_read_in_algorithms) > 0:
            self.set_read_in_algorithm(list(self.all_read_in_algorithms.keys())[0])
        else:
            self.read_in_algorithm = None
            messagebox.showwarning('warning', 'no read in algorithm found')
        self.all_evaluation_algorithms = evaluation_algorithms.get_all_algorithms()
        if len(self.all_evaluation_algorithms) > 0:
            self.set_evaluation_algorithm(list(self.all_evaluation_algorithms.keys())[0])
        else:
            self.evaluation_algorithm = None
            messagebox.showwarning('warning', 'found no evaluation algorithm')

        self.default_settings()

    def set_read_in_algorithm(self, algorithm):#otherwise no lambda expression in Gui for that possible
        self.read_in_algorithm = algorithm

    def find_best_shape(self):
        best_shape = []
        for generation in self.generations:
            for shp in generation:
                if not best_shape or shp.fittness > best_shape[0].fittness:
                    best_shape.append(shp)
                elif best_shape[0].fittness != None and shp.fittness == best_shape[0].fittness:
                    best_shape.append(shp)

    def set_optimization_running(self, running: bool):
        with self.lock:
            self.optimization_running = running

    def get_optimization_running(self):
        with self.lock:
            return self.optimization_running

    def set_evaluation_algorithm(self, algorithm):#otherwise no lambda expression in Gui for that possible
        self.evaluation_algorithm = algorithm

    def start_optimization(self):
        print('start optimization')
        if not [algorithm for algorithm in self.mutation_algorithms if algorithm.activated]:
            messagebox.showerror('error', 'no active mutation algorithm')
            raise MissingAlgorithmException('no activated mutation algorithm')
        if not [algorithm for algorithm in self.pairing_algorithms if algorithm.activated]:
            messagebox.showerror('error', 'no active pairing algorithm')
            raise MissingAlgorithmException('no activated pairing algorithm')
        if not self.mentat_connections:
            messagebox.showerror('error', 'no Mentat instance connected.')
            raise NoMentatConnectionException

        if not self.generations:
            self.evaluate_shapes([self.inital_shape])
            self.generate_first_generation()
            self.improvement_history.clear()

        while self.optimization_running:
            generation = self.generations[-1]
            self.evaluate_shapes(generation)
            self.save_improvement(generation,self.generations.index(generation))
            self.generations.append(self.build_next_generation(generation))

    def save_improvement(self,generation,gen_num):
        fittnesses = []
        for shp in generation:
            fittnesses.append(shp.fittness)
        mean_fittness = stat.mean(fittnesses)
        max_fittness = max(fittnesses)
        min_fittness = min(fittnesses)
        self.improvement_history.append([gen_num,fittnesses,mean_fittness,max_fittness,min_fittness])



    def build_next_generation(self, generation):
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
            pairing_algorithm = random.choice([algorithm for algorithm in self.pairing_algorithms if algorithm.activated])
            new_shape = pairing_algorithm.pair_shapes(shape1,shape2)
            next_generation.append(new_shape)
        next_generation.append(np.random.choice(generation, p=normalized_fittness))
        return next_generation
        

    def generate_first_generation(self): #fills the first array of self.generations with random shapes
        """Generates a generation of random shapes
        
        Fills the first position in the list self.generations with a list of random shapes called the inital generation
        """
        self.generations = []#maybe bad
        generation = []
        activated_mutation_algorithms = [algorithm for algorithm in self.mutation_algorithms if algorithm.activated]

        if not self.inital_shape:
            messagebox.showerror('error', 'no initial shape')
            raise MissingInitialShapeException

        else:
            for _ in range(self.first_generation_size):
                algorithm = random.choice(activated_mutation_algorithms)
                shp = algorithm.change_shape(self.inital_shape)
                generation.append(shp)
            self.generations.append(generation)

    def default_settings(self):
        """Sets the settings of itself to the default settings
        """
        self.first_generation_size = 3

    def mutate_shape(self,algorithm):
        pass

    def evaluate_shapes(self, shapes):#in genera probably better to use a Queue
        '''takes a list of shapes, e.g. a gereration and evaluates them using one solver thread for each connected Mentat instance'''
        def mentat_connection_loop(tasklist, connection):
            HOST, PORT = connection
            task, index = tasklist.get_next_task()
            while not (task is None):
                print(connection, 'does the task with index ', index)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:#maybe first try a testobject as the failure of connection might not be detected without timeout(but I am not quite sure)
                        s.connect((HOST, PORT))
                        obj_bytes = pickle.dumps(task)

                        if len(str(len(obj_bytes)))>HEADERSIZE:
                            raise Exception('Length of the object to send exceeds header size. Increase HEADERSIZE')
                        
                        header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
                        s.sendall(header + obj_bytes)

                        obj_recv = bytearray()
                        data = s.recv(64)
                        obj_length = int(data[:HEADERSIZE].decode('utf-8'))
                        obj_recv.extend(data[HEADERSIZE:])
                        while len(obj_recv) < obj_length:
                            data = s.recv(64)
                            obj_recv.extend(data)

                        result = pickle.loads(obj_recv)
                        print(connection, 'returns the task with index', index, ' and result ', result)
                        tasklist.return_evaluation(index, True, result)
                    except socket.error as e:
                        print('fatal exception in one of the connections with mentat')
                        tasklist.return_evaluation(index, False)
                        break
                    task, index = tasklist.get_next_task()

        tasklist = mentat_connection.Tasklist(shapes, self.all_read_in_algorithms[self.read_in_algorithm], self.all_evaluation_algorithms[self.evaluation_algorithm])

        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(self.mentat_connections)) as executor:
            for connection in self.mentat_connections:
                print(connection, 'is starting')
                executor.submit(mentat_connection_loop, tasklist, connection)#exceptions might not be visible!!!

        for evaluation in tasklist.evaluations:#test if tasklist was completely evaluated
            if isinstance(evaluation, str):
                print('wrong tasklist', tasklist.evaluations)
                raise Exception('tasklist not evaluated correctly')
        
        print('the evaluation took {} seconds'.format(time.time()-start_time))
        print('the evaluation list: ', tasklist.evaluations)

        for i, shape in enumerate(shapes):
            shape.fittness = tasklist.evaluations[i]


class MissingAlgorithmException(Exception):
    pass

class MissingInitialShapeException(Exception):
    pass

class NoMentatConnectionException(Exception):
    pass