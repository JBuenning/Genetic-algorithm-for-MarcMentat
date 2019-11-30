import random
import pickle
import threading

HEADERSIZE = 20

#die Instanzen der hier definierten Klassen werden vom Hauptprogramm zu Mentat geschickt
#dort wird das Objekt entpackt und die methode execute aufgerufen

class Simple_task:
    def __init__(self, shape, evaluation_algorithm):
        self.evaluation_argorithm = evaluation_algorithm
        self.shape_area = shape.area
        self.shape_coords = list(shape.exterior.coords[:-1])

    def execute(self, py_mentat, py_post, socket_connection):
        print('execuuuuuuuutinggggggggggg')
        self.evaluation_argorithm.execute('', py_mentat, py_post, socket_connection)

class Task:
    def __init__(self, shape, read_in_algorithm, evaluation_algorithm):
        self.shape_area = shape.area
        self.shape_coords = list(shape.exterior.coords[:-1])
        self.shape_fixed_displacements = shape.fixed_displacements
        self.shape_forces = shape.forces
        self.read_in_algorithm = read_in_algorithm
        self.evaluation_algorithm = evaluation_algorithm

    def execute(self, py_mentat, py_post, socket_connection):

        self.read_in_algorithm.execute(self.shape_coords, self.shape_fixed_displacements, self.shape_forces, py_mentat)
        self.evaluation_algorithm.execute(self.shape_coords, self.shape_area, py_mentat, py_post, socket_connection)

        #this was the read in part
        # py_mentat.py_send('*clear_geometry')
        # py_mentat.py_send('*clear_mesh')
        # for point in self.coords:
        #     py_mentat.py_send("*add_points {},{},0".format(point[0], point[1]))

        # py_mentat.py_send('*set_curve_type line')

        # for i in range(1, len(self.coords)):
        #     py_mentat.py_send('*add_curves {},{}'.format(i, i+1))
        # py_mentat.py_send('*add_curves {},1'.format(len(self.coords)))

        # obj_bytes = pickle.dumps('evaluation')# hier wird später der ermittelte Wert zurückgesendet
        # if len(str(len(obj_bytes)))>HEADERSIZE:
        #     raise Exception('Length of the object to send exceeds header size')
        
        # header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
        # socket_connection.sendall(header + obj_bytes)

class Test_connection:
    def __init__(self, testobject):
        self.testobject = testobject
        
    def execute(self, py_mentat, py_post, socket_connection):
        obj_bytes = pickle.dumps(self.testobject)

        if len(str(len(obj_bytes)))>HEADERSIZE:
            raise Exception('Length of the object to send exceeds header size')
        
        header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
        socket_connection.sendall(header + obj_bytes)

class Tasklist:
    def __init__(self, shapes, read_in_algorithm, evaluation_algorithm):
        self.read_in_algorithm = read_in_algorithm
        self.evaluation_algorithm = evaluation_algorithm
        self.shapes = shapes
        self.evaluations = ['not evaluating']*len(shapes)#not evaluating, <value> or evaluating
        self.lock = threading.Lock()

    def return_evaluation(self, index, success, evaluation_value=None):
        with self.lock:
            if success:
                self.evaluations[index] = evaluation_value
            else:
                self.evaluations[index] = 'not evaluating'

    def get_next_task(self):
        '''returns the task or None if there is no task left'''
        with self.lock:
            for i, evaluation in enumerate(self.evaluations):#maybe wrong!!!!!
                if evaluation == 'not evaluating':
                    task = Task(self.shapes[i], self.read_in_algorithm, self.evaluation_algorithm)
                    self.evaluations[i] = 'evaluating'
                    return (task, i)

            return (None, 99999)
                #maybe good thing to add an else statement, where tasks that are already evaluating are evaluated multiple times so that
                #slow machines can not slwo down the process
