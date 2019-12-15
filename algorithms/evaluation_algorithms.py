import tkinter as tk
import pickle

def get_all_algorithms():#to be improved
    '''returns dictionary with all algorithms'''
    algo_list = [Min_stress_min_area()]
    algo_dict = {}
    for algo in algo_list:
        algo_dict[algo.get_name()] = algo
    
    return algo_dict

class Evaluation_algorithm:

    def execute(self, shape_coords, shape_area, py_mentat, py_post, connection):
        raise NotImplementedError
        #must return evaluation!!!!!!

    def get_name(self):
        raise NotImplementedError

    def get_settings_frame(self, master):
        frame = tk.Frame()
        label = tk.Label(frame, text='no settings available')
        label.pack()
        return frame

    def send_result(self, result, connection):
        '''sends the calculated fittness back. The result should be of type float/int'''
        HEADERSIZE = 20#not dynamic! To be fixed

        obj_bytes = pickle.dumps(result)

        if len(str(len(obj_bytes)))>HEADERSIZE:
            raise Exception('Length of the object to send exceeds header size')
        
        header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
        connection.sendall(header + obj_bytes)

class Min_stress_min_area(Evaluation_algorithm):

    def get_name(self):
        return 'min stress min area'

    def execute(self, shape_coords,shape_length, shape_area, py_mentat, py_post, connection):
        print('evaluating shape')
        py_mentat.py_send('*post_open_default')
        py_mentat.py_send('*post_value Equivalent Von Mises Stress')
        py_mentat.py_send('*post_contour_bands')
        n_id = py_mentat.py_get_int("scalar_max_node()")
        max_von_mises_stress = py_mentat.py_get_float('scalar_1({})'.format(n_id))

        if max_von_mises_stress:#check if something went wrong
            #print('the maximal Von Mises Stress is ', max_von_mises_stress)
            result = 1/max_von_mises_stress#just for testing
        else:
            print('something went wrong')
            result = shape_area/shape_length
            #result = -99999

        #......actual result must be calculated

        self.send_result(result, connection)
