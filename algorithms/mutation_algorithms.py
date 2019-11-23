import shape
import tkinter
import random

def get_all_mutation_algorithms():
    array = []
    one = AlgorithmOne()
    array.append(one)
    return array

class MutationAlgorithm:
    def __init__(self):
        self.name = self.get_name()
        self.default_settings()
        self.activated = True
    
    def change_shape(self, shape):
        raise NotImplementedError

    def default_settings(self):
        raise NotImplementedError

    def get_settings_frame(self, master): #has to return settings_frame
        frame = tkinter.Frame(master)
        label = tkinter.Label(frame, text='no settings available')
        label.pack()
        frame.pack()
        return frame

    def get_name(self):
        raise NotImplementedError

    def get_description(self):
        return 'no descriptin available'

class AlgorithmOne(MutationAlgorithm):
#zufällige Form
#max_movement - in prozent bezogen auf abstand beider nachbarpunkte zueinander
#min_movement - siehe max


    def default_settings(self):
        self.min_movement=0.1
        self.max_movement=1
        self.max_recursiondepth=20

    def change_shape(self, shp, endless_loop_counter=0):
    #min und max movement beziehen sich auf die Distanz zwischen den Nachbarpunkten.
    #ein movement von 1 würde bedeuten, dass der Punkt sich um die Länge der Entfernung der Nachbarpunkte zueinander bewegt
    #erst mal nur für das Äußere

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
                    print('round shape')
                    return self.change_shape(shape.round_shape(shp), 0)
                else:
                    print('das sollte besser nicht zu oft hintereinander zu sehen sein')
                    return self.change_shape(shp,endless_loop_counter+1)

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

    def get_name(self):
        return 'Algorithm One'

    
    
    