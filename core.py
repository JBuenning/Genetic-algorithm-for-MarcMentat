import shape
import examples
import mentat_connection
from mentat_connection import HEADERSIZE, Test_connection, Simple_task
import random
from algorithms import mutation_algorithms, read_in_algorithms, evaluation_algorithms
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
import socket
import pickle
import threading


class Core:
    def __init__(self):
        self.generations = [] #list with all generations, generation[0] is the inital generation
        self.inital_shape = None #Shape that the user wants to improve
        self.mutation_algorithms = mutation_algorithms.get_all_mutation_algorithms()
        self.mentat_connections = []
        #self.mentat_commands = [] #replaced by read_in and evaluation algorighm
        self.all_read_in_algorithms = read_in_algorithms.get_all_algorithms()
        if len(self.all_read_in_algorithms) > 0:
            self.set_read_in_algorithm(list(self.all_read_in_algorithms.keys())[0])
        else:
            self.read_in_algorithm = None
            messagebox.showwarning('warning', 'found no read in algorithm')
        self.all_evaluation_algorithms = evaluation_algorithms.get_all_algorithms()
        if len(self.all_evaluation_algorithms) > 0:
            self.set_evaluation_algorithm(list(self.all_evaluation_algorithms.keys())[0])
        else:
            self.evaluation_algorithm = None
            messagebox.showwarning('warning', 'found no evaluation algorithm')

        self.default_settings()

    def set_read_in_algorithm(self, algorithm):#otherwise no lambda expression in Gui for that possible
        self.read_in_algorithm = algorithm

    def set_evaluation_algorithm(self, algorithm):#otherwise no lambda expression in Gui for that possible
        self.evaluation_algorithm = algorithm

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
            HOST, PORT = connection
            task, index = tasklist.get_next_task()
            while not (task is None):

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
                        tasklist.return_evaluation(index, True, result)
                    except socket.error as e:
                        print('fatal exception in one of the connections with mentat')
                        tasklist.return_evaluation(index, False)
                        break
                    task, index = tasklist.get_next_task()

        tasklist = mentat_connection.Tasklist(shapes, self.all_read_in_algorithms[self.read_in_algorithm], self.all_evaluation_algorithms[self.evaluation_algorithm])

        with ThreadPoolExecutor(max_workers=len(self.mentat_connections)) as executor:
            for connection in self.mentat_connections:
                executor.submit(mentat_connection_loop, tasklist, connection)#exceptions might not be visible!!!

        for evaluation in tasklist.evaluations:#test if tasklist was completely evaluated
            if isinstance(evaluation, str):
                print('wrong tasklist', tasklist.evaluations)
                raise Exception('tasklist not evaluated correctly')
        
        print('the evaluation list:\n', tasklist.evaluations)
        return tasklist.evaluations
        