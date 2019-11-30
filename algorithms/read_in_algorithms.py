import tkinter as tk

def get_all_algorithms():#to be improved
    '''returns dictionary with all algorithms'''
    algo_list = [Basic_read_in()]
    algo_dict = {}
    for algo in algo_list:
        algo_dict[algo.get_name()] = algo
    
    return algo_dict


class Read_in_algorithm:

    def execute(self, shape_coords, py_mentat):
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

    def execute(self, shape_coords, py_mentat):
        print('something is read in')
        pass
