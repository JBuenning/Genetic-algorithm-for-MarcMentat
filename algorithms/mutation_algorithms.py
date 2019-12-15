import shape
import tkinter as tk
from tkinter import ttk
import random
from algorithms import algorithm
import math

def get_all_mutation_algorithms():
    """Returns an object of every mutation algorithm presen in this file
    
    Returns:
        list: Contains one object of evers mutation algorithm
    """
    lst = [AlgorithmOne(),AlgorithmTwo()]
    return lst

class MutationAlgorithm(algorithm.Algorithm):

    def change_shape(self, shp):
        """Changes a shape randomly
        
        Args:
            shp (shape): Will be changed
        
        Raises:
            NotImplementedError: If not overwritten
        """
        raise NotImplementedError


class AlgorithmOne(MutationAlgorithm):
#zufällige Form
#max_movement - in prozent bezogen auf abstand beider nachbarpunkte zueinander
#min_movement - siehe max

    def default_settings(self):
        self.min_movement=0.1
        self.max_movement=1.0
        self.max_recursiondepth=20
        self.n_times = 20
    
    def set_default(self):# erklären lassen von jonas
        self.default_settings()
        self.ent_min_movement.delete(0,'end')
        self.ent_min_movement.insert(0, self.min_movement)
        self.ent_max_movement.delete(0,'end')
        self.ent_max_movement.insert(0, self.max_movement)
        self.ent_max_recursiondepth.delete(0,'end')
        self.ent_max_recursiondepth.insert(0, self.max_recursiondepth)
        self.ent_n_times.delete(0, 'end')
        self.ent_n_times.insert(0, self.n_times)

    def apply(self):
        try:
            self.min_movement = float(self.ent_min_movement.get())
            self.ent_min_movement.delete(0, 'end')
            self.ent_min_movement.insert(0, self.min_movement)
        except:
            self.ent_min_movement.delete(0, 'end')
            self.ent_min_movement.insert(0, self.min_movement)
        try:
            self.max_movement = float(self.ent_max_movement.get())
            self.ent_max_movement.delete(0, 'end')
            self.ent_max_movement.insert(0, self.max_movement)
        except:
            self.ent_max_movement.delete(0, 'end')
            self.ent_max_movement.insert(0, self.max_movement)
        try:
            self.max_recursiondepth = int(self.ent_max_recursiondepth.get())
            self.ent_max_recursiondepth.delete(0, 'end')
            self.ent_max_recursiondepth.insert(0, self.max_recursiondepth)
        except:
            self.ent_max_recursiondepth.delete(0, 'end')
            self.ent_max_recursiondepth.insert(0, self.max_recursiondepth)
        try:
            self.n_times = int(self.ent_n_times.get())
            self.ent_n_times.delete(0, 'end')
            self.ent_n_times.insert(0, self.n_times)
        except:
            self.ent_n_times.delete(0, 'end')
            self.ent_n_times.insert(0, self.n_times)

    def get_settings_frame(self, master):

        frame = tk.Frame(master)
        tk.Label(frame, text='min movement').grid(row=0, column=0, sticky='w')
        self.ent_min_movement = tk.Entry(frame, width=5)
        self.ent_min_movement.grid(row=0, column=1)
        tk.Label(frame, text='max movement').grid(row=1, column=0, sticky='w')
        self.ent_max_movement = tk.Entry(frame, width=5)
        self.ent_max_movement.grid(row=1, column=1)
        tk.Label(frame, text='max recursion depth').grid(row=2, column=0, sticky='w')
        self.ent_max_recursiondepth = tk.Entry(frame, width=5)
        self.ent_max_recursiondepth.grid(row=2, column=1)
        tk.Label(frame, text='repetitions').grid(row=3, column=0, sticky='w')
        self.ent_n_times = tk.Entry(frame, width=5)
        self.ent_n_times.grid(row=3, column=1)
        apply = ttk.Button(frame, text='apply', command=self.apply)
        apply.grid(row=4, column=0, pady=4)
        default = ttk.Button(frame, text='reset', command=self.set_default)
        default.grid(row=4, column=1, pady=4)
        self.set_default()
        return frame

    def change_shape(self, shp):
    #min und max movement beziehen sich auf die Distanz zwischen den Nachbarpunkten.
    #ein movement von 1 würde bedeuten, dass der Punkt sich um die Länge der Entfernung der Nachbarpunkte zueinander bewegt
    #erst mal nur für das Äußere

        def help(shp, endless_loop_counter=0):
            coords = shp.exterior.coords[:-1]
            coords_neg = shp.exterior.coords[:-1]
            random_selection = []
            for i in range(len(coords)):
                if (not shp.move_restrictions[i]) or (type(shp.move_restrictions[i]) is tuple):
                    random_selection.append(i)
            choice = random.choice(random_selection)
            if choice == len(coords)-1:
                n2 = 0
            else:
                n2 = choice+1
            n1 = choice - 1

            movement = random.uniform(self.min_movement, self.max_movement)
            movement_neg = movement * (-1)
            coords[choice] = shape.move_point(coords[choice], coords[n1], coords[n2], movement, shp.move_restrictions[choice])
            coords_neg[choice] = shape.move_point(coords_neg[choice], coords_neg[n1], coords_neg[n2], movement_neg, shp.move_restrictions[choice])
            s = shape.Shape(coords, shp.interiors, shp.move_restrictions, shp.fixed_displacements, shp.forces)
            s = shape.even_out_shape(s, 3)
            s_neg = shape.Shape(coords_neg, shp.interiors, shp.move_restrictions, shp.fixed_displacements, shp.forces)
            s_neg = shape.even_out_shape(s_neg, 3)
            while (not s.is_valid) or (not s.is_simple) or (not s_neg.is_valid) or (not s_neg.is_simple):
                if movement <= self.min_movement:
                    if endless_loop_counter >= self.max_recursiondepth:
                        return help(shape.round_shape(shp), 0)
                    else:
                        return help(shp,endless_loop_counter+1)

                else:
                    coords = shp.exterior.coords[:-1]
                    coords_neg = shp.exterior.coords[:-1]
                    movement = movement/2
                    movement_neg = movement_neg/2
                    coords[choice] = shape.move_point(coords[choice], coords[n1], coords[n2], movement, shp.move_restrictions[choice])
                    coords_neg[choice] = shape.move_point(coords_neg[choice], coords_neg[n1], coords_neg[n2], movement_neg, shp.move_restrictions[choice])
                    s = shape.Shape(coords, shp.interiors, shp.move_restrictions, shp.fixed_displacements, shp.forces)
                    s = shape.even_out_shape(s, 3)
                    #s = round_shape(s, 1)
                    s_neg = shape.Shape(coords_neg, shp.interiors, shp.move_restrictions, shp.fixed_displacements, shp.forces)
                    s_neg = shape.even_out_shape(s_neg, 3)
                    #s_neg =round_shape(s_neg, 1)
            return random.choice([s, s_neg])
        
        for _ in range(self.n_times):
            shp = help(shp)
        
        return shp

    def get_name(self):
        return 'Algorithm One'

class AlgorithmTwo(MutationAlgorithm):

    def change_shape(self,shp):
        def move_point(point, start, end, movement, restriction):
            sx, sy = start
            ex, ey = end
            px, py = point
            if restriction:
                if type(restriction) is tuple:
                    movement_x, movement_y = restriction
                else:
                    pass
            else:
                movement_x = ey - sy
                movement_y = sx - ex

            movement = movement * (math.sqrt(math.pow(movement_x, 2) + math.pow(movement_y, 2))/math.sqrt(math.pow(ex-sx, 2) + math.pow(ey-sy, 2)))

            x = px + movement*movement_x
            y = py + movement*movement_y
            return (x,y)

        def linear_function(shp,coords_change):
            ### Lineare Funktion ###
            coords = shp.exterior.coords[:-1]
            start_coord = coords_change[0]
            end_coord = coords_change[len(coords_change)-1]
            in_or_out = random.choice([-1,1])
            if (len(coords_change) % 2) != 0:
                r=0
                start_len = end_len = int(len(coords_change)/2)+1
            else:
                r = random.randint(0,1)
                if bool(r):
                    start_len = int(len(coords_change)/2)
                    end_len = int(len(coords_change)/2)+1
                else:
                    start_len = int(len(coords_change)/2)+1
                    end_len = int(len(coords_change)/2)
            #mid_coord = coords_change[int((len(coords_change)/2))-r]
            for i in range(start_len):
                coords[coords.index(coords_change[i])] = move_point(coords_change[i],start_coord,end_coord,(i/(start_len-1))*0.1*in_or_out,False)
            for i in range(end_len-1):
                coords[coords.index(coords_change[len(coords_change)-1-i])] = move_point(coords_change[len(coords_change)-1-i],start_coord,end_coord,(i/(start_len-1))*0.1*in_or_out,False)
            return shape.Shape(coords, shp.interiors, shp.move_restrictions, shp.fixed_displacements, shp.forces)
        def help(shp):
            ### Zu ändernde Koordinaten werden bestimmt ###
            coords = shp.exterior.coords[:-1]
            coords_free = []
            coords_change = []
            min_num_changed_coords = 1
            for i, coord in enumerate(coords):
                if shp.move_restrictions[i] == False: #später anpassen auf teilweise eingeschränkte Punkte
                    coords_free.append(coord)
            start = random.randint(0,int(len(coords_free)/2))#int(len(coords2)/2) nur zum ausprobieren kann auch anders gewählt werden
            for i in range(start,random.randint(start+min_num_changed_coords+2,len(coords_free)-1)):#len(coords_free)-1 eventuell stärker eingrenzen
                coords_change.append(coords_free[i])
            
            ### Umformung ###
            s = linear_function(shp,coords_change)

            ### Kontrollen ###
            while not(s.is_valid) or not(s.is_simple) or not(s.is_thick()):
                s = self.change_shape(shp)

            ### Glätten ###
            s = shape.even_out_shape(s, 3)
            return s
        
        for _ in range(self.n_times):
            shp = help(shp)
        return shp

    
    def get_name(self):
        return 'Algorithm Two'
    
    def default_settings(self):
        self.n_times = 1
    
    def set_default(self):# erklären lassen von jonas
        self.default_settings()
        self.ent_n_times.delete(0, 'end')
        self.ent_n_times.insert(0, self.n_times)
    
    def apply(self):
        try:
            self.n_times = int(self.ent_n_times.get())
            self.ent_n_times.delete(0, 'end')
            self.ent_n_times.insert(0, self.n_times)
        except:
            self.ent_n_times.delete(0, 'end')
            self.ent_n_times.insert(0, self.n_times)
    
    def get_settings_frame(self, master):
        frame = tk.Frame(master)
        tk.Label(frame, text='repetitions').grid(row=3, column=0, sticky='w')
        self.ent_n_times = tk.Entry(frame, width=5)
        self.ent_n_times.grid(row=3, column=1)
        apply = ttk.Button(frame, text='apply', command=self.apply)
        apply.grid(row=4, column=0, pady=4)
        default = ttk.Button(frame, text='reset', command=self.set_default)
        default.grid(row=4, column=1, pady=4)
        self.set_default()
        return frame