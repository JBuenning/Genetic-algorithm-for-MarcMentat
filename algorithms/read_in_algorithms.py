import tkinter as tk
import time

def get_all_algorithms():#to be improved
    '''returns dictionary with all algorithms'''
    algo_list = [Basic_read_in()]
    algo_dict = {}
    for algo in algo_list:
        algo_dict[algo.get_name()] = algo
    
    return algo_dict


class Read_in_algorithm:

    def execute(self, shape_coords, shape_fixed_dispacements, shape_forces, py_mentat):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_settings_frame(self, master):
        frame = tk.Frame()
        label = tk.Label(frame, text='no settings available')
        label.pack()
        return frame

class Basic_read_in(Read_in_algorithm):

    def get_name(self):
        return 'basic read in algorithm'

    def execute(self, shape_coords, shape_fixed_dispacements, shape_forces, py_mentat):
        print('something is read in')
        py_mentat.py_send('*new_model yes')
        for point in shape_coords:
            py_mentat.py_send("*add_points {},{},0".format(point[0], point[1]))

        py_mentat.py_send('*set_curve_type line')

        for i in range(1, len(shape_coords)):
            py_mentat.py_send('*add_curves {},{}'.format(i, i+1))
        py_mentat.py_send('*add_curves {},1'.format(len(shape_coords)))
        time.sleep(1)#for simulating complicated task
