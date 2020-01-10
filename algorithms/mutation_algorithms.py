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
    lst = [AlgorithmOne(), AlgorithmTwo()]
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

    def get_name(self):
        return 'Algorithm two'

    def default_settings(self):
        self.min_movement = 1.0
        self.max_movement = 100.0
        self.min_radius = 0.0 #in this case like Algorithm one
        self.max_radius = 20.0
        self.max_recursiondepth=20
        self.n_times = 20
        self.editing_mode = 'smooth'

    def set_default(self):# button-click
        self.default_settings()
        self.ent_min_movement.delete(0,'end')
        self.ent_min_movement.insert(0, self.min_movement)
        self.ent_max_movement.delete(0,'end')
        self.ent_max_movement.insert(0, self.max_movement)
        self.ent_min_radius.delete(0, 'end')
        self.ent_min_radius.insert(0, self.min_radius)
        self.ent_max_radius.delete(0, 'end')
        self.ent_max_radius.insert(0, self.max_radius)
        self.ent_max_recursiondepth.delete(0,'end')
        self.ent_max_recursiondepth.insert(0, self.max_recursiondepth)
        self.ent_n_times.delete(0, 'end')
        self.ent_n_times.insert(0, self.n_times)
        self.ent_editing_mode.current(0)

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
            self.min_radius = float(self.ent_min_radius.get())
            self.ent_min_radius.delete(0, 'end')
            self.ent_min_radius.insert(0, self.min_radius)
        except:
            self.ent_min_radius.delete(0, 'end')
            self.ent_min_radius.insert(0, self.min_radius)

        try:
            self.max_radius = float(self.ent_max_radius.get())
            self.ent_max_radius.delete(0, 'end')
            self.ent_max_radius.insert(0, self.max_radius)
        except:
            self.ent_max_radius.delete(0, 'end')
            self.ent_max_radius.insert(0, self.max_radius)
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
        
        self.editing_mode = self.ent_editing_mode.get()

    def get_settings_frame(self, master):
        frame = tk.Frame(master)
        tk.Label(frame, text='min movement').grid(row=0, column=0, sticky='w')
        self.ent_min_movement = tk.Entry(frame, width=5)
        self.ent_min_movement.grid(row=0, column=1)
        tk.Label(frame, text='max movement').grid(row=1, column=0, sticky='w')
        self.ent_max_movement = tk.Entry(frame, width=5)
        self.ent_max_movement.grid(row=1, column=1)

        tk.Label(frame, text='min radius').grid(row=2, column=0, sticky='w')
        self.ent_min_radius = tk.Entry(frame, width=5)
        self.ent_min_radius.grid(row=2, column=1)

        tk.Label(frame, text='max radius').grid(row=3, column=0, sticky='w')
        self.ent_max_radius = tk.Entry(frame, width=5)
        self.ent_max_radius.grid(row=3, column=1)

        tk.Label(frame, text='max recursion depth').grid(row=4, column=0, sticky='w')
        self.ent_max_recursiondepth = tk.Entry(frame, width=5)
        self.ent_max_recursiondepth.grid(row=4, column=1)
        tk.Label(frame, text='repetitions').grid(row=5, column=0, sticky='w')
        self.ent_n_times = tk.Entry(frame, width=5)
        self.ent_n_times.grid(row=5, column=1)
        tk.Label(frame, text='editing mode').grid(row=6, column=0, sticky='w')
        self.ent_editing_mode = tk.ttk.Combobox(frame, values=['smooth', 'linear', 'constant', 'sharp', 'root', 'sphere'], state='readonly')
        self.ent_editing_mode.grid(row=6, column=1)
        apply = ttk.Button(frame, text='apply', command=self.apply)
        apply.grid(row=7, column=0, pady=4)
        default = ttk.Button(frame, text='reset', command=self.set_default)
        default.grid(row=7, column=1, pady=4)
        self.set_default()
        return frame

    def change_shape(self, shp):
        
        def help(shp, loop_counter=0):

            #see https://blender.stackexchange.com/questions/98487/what-is-the-algorithm-behind-blenders-proportional-edit/98505
            def linear(radius, distance):
                return 1 - (distance/radius)

            def constant(radius, distance):
                return 1

            def sharp(radius, distance):
                return (1 - (distance/radius)) ** 2
            
            def root(radius, distance):
                return math.sqrt(1 - (distance/radius))

            def sphere(radius, distance):
                return math.sqrt((1 - (distance/radius))*2 - (1 - (distance/radius))**2)

            def smooth(radius, distance):
                return 3*((1 - (distance/radius))**2) - 2*((1 - (distance/radius))**3)

            if self.editing_mode == 'smooth':
                falloff = smooth
            elif self.editing_mode == 'sphere':
                falloff = sphere
            elif self.editing_mode == 'root':
                falloff = root
            elif self.editing_mode == 'sharp':
                falloff = sharp
            elif self.editing_mode == 'constant':
                falloff = constant
            elif self.editing_mode == 'linear':
                falloff = linear

            success = False

            while not success:

                coords = shp.exterior.coords[:-1]
                movable_points = []
                for i in range(len(coords)):
                    if (not shp.move_restrictions[i]) or (type(shp.move_restrictions[i]) is tuple):
                        movable_points.append(i)

                choice = random.choice(movable_points)
                radius = random.uniform(self.min_radius, self.max_radius)
                movement = random.uniform(self.min_movement, self.max_movement) * random.choice([1, -1])

                n1 = choice -1
                if choice == len(coords)-1:
                    n2 = 0
                else:
                    n2 += 1
                new_point = shape.move_point(coords[choice], coords[n1], coords[n2], movement, shp.moverestrictions[choice])
                movement_x = new_point[0] - coords[choice][0]
                movement_y = new_point[1] - coords[choice][1]
                coords[choice] = new_point

                #positive
                if choice == len(coords)-1:
                    target = 0
                else:
                    target = choice + 1

                distance = shape.distance(coords[target], coords[choice])
                while distance < radius:
                    new_x = coords[target][0] + movement_x*falloff(radius, distance)
                    new_y = coords[target][1] + movement_y*falloff(radius, distance)
                    coords[target] = (new_x, new_y)
                    if target == len(coords)-1:
                        new_target = 0
                    else:
                        new_target = target + 1

                    distance += shape.distance(coords[target], coords[new_target])
                    target = new_target
                
                #negative
                target = choice - 1

                distance = shape.distance(coords[target], coords[choice])
                while distance < radius:
                    new_x = coords[target][0] + movement_x*falloff(radius, distance)
                    new_y = coords[target][1] + movement_y*falloff(radius, distance)
                    coords[target] = (new_x, new_y)
                    new_target = target - 1

                    distance += shape.distance(coords[target], coords[new_target])
                    target = new_target

                s = shape.Shape(coords, shp.interiors, shp.move_restrictions, shp.fixed_displacements, shp.forces)
                s = shape.even_out_shape(s, 3)

                success = s.is_valid and s.is_simple

            return s



        for _ in range(self.n_times):
            shp = help(shp)

        return shp

    
    
    