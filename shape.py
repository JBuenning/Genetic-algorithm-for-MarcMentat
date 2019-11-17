from shapely import geometry
import matplotlib.pyplot as plt
import numpy as np
import random
import math


def get_realistic_example():
    shell = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),
             (14,1),(14,2),(14,3),
             (13,3),(12,3),(11,3),(10,3),(9,3),(8,3),(7,3),(6,3),(5,3),(4,3),(3,3),
             (3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(3,12),(3,13),
             (3,14),(2,14),(1,14),
             (0,14),(0,13),(0,12),(0,11),(0,10),(0,9),(0,8),(0,7),(0,6),(0,5),(0,4),(0,3),(0,2),(0,1)]

    move_restrictions = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,
                         True,True,True,
                         False,False,False,False,False,False,False,False,False,False,False,
                         False,False,False,False,False,False,False,False,False,False,
                         True,True,True,
                         True,True,True,True,True,True,True,True,True,True,True,True,True,True]

    return Shape(shell, move_restrictions=move_restrictions)

#n_times - wie oft soll der algorithmus laufen
#Algorithmus macht gleiche Abstände zwischen Punkten ohne Fläche und Form stark zu verändern
def even_out_shape(shape, n_times=1):

    def even_out_point(point, neighbour1, neighbour2, restriction):
        #hilfsfunktion für even_out_shape
        px, py = point
        n1x, n1y = neighbour1
        n2x, n2y = neighbour2
        mx = (n2x + n1x)/2#mitte zwischen den Nachbarpunkten
        my = (n2y + n1y)/2
        
        if restriction:
            if type(restriction) is tuple:
                restriction_x, restriction_y = restriction
                #in Matrixschreibweise AX=B
                try:
                    A = np.array([[restriction_x, n1y-n2y],[restriction_y, n2x-n1x]])
                    B = np.array([mx-px, my-py])
                    t,u = np.linalg.solve(A,B)

                    x = px + t*(restriction_x)
                    y = py + t*(restriction_y)
                except:
                    #wenn der Punkt sich wegen der restriction nur senkrecht zu den Nachbarpunkten bewegen dürfte
                    x, y = point
            else:
                x, y = point

        else:
            #in Matrixschreibweise AX=B
            A = np.array([[n2x-n1x, n1y-n2y],[n2y-n1y, n2x-n1x]])
            B = np.array([mx-px, my-py])
            t,u = np.linalg.solve(A,B)

            x = px + t*(n2x - n1x)
            y = py + t*(n2y - n1y)
        return(x,y)
    #bisher nur äussere form
    coords = shape.exterior.coords[:-1]
    for i in range(len(coords)):
        coords[i-1] = even_out_point(coords[i-1], coords[i], coords[i-2], shape.move_restrictions[i-1])

    shape = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    if n_times == 1:
        return shape
    else:
        return even_out_shape(shape, n_times - 1)

def change_shape_two(shape, min_movement=0.1, max_movement=1):
    coords = shape.exterior.coords[:-1]
    coords_free = []
    coords_change = []
    min_num_changed_coords = 1
    for i, coord in enumerate(coords):
        if shape.move_restrictions[i] == False: #später anpassen auf teilweise eingeschränkte Punkte
            coords_free.append(coord)
    start = random.randint(0,int(len(coords_free)/2))#int(len(coords2)/2) nur zum ausprobieren kann auch anders gewählt werden
    for i in range(start,random.randint(start+min_num_changed_coords+2,len(coords_free)-1)):#len(coords_free)-1 eventuell stärker eingrenzen
        coords_change.append(coords_free[i])
    start_coord = coords_change[0]
    end_coord = coords_change[len(coords_change)-1]
    mid_coord = coords_change[int((len(coords_change)-1)/2)+random.randint(0,1)]
    return shape

#zufällige Form
#max_movement - in prozent bezogen auf abstand beider nachbarpunkte zueinander
#min_movement - siehe max
def change_shape_simple(shape, min_movement=0.1, max_movement=1, n_times=1):
    def move_point(point, neighbour1, neighbour2, movement, restriction):
        #Hilfsfuntion für change_shape
        n1x, n1y = neighbour1
        n2x, n2y = neighbour2
        px, py = point
        if restriction:
            if type(restriction) is tuple:
                movement_x, movement_y = restriction
            else:
                return point
        else:
            movement_x = n2y - n1y
            movement_y = n1x - n2x

        movement = movement * (math.sqrt(math.pow(movement_x, 2) + math.pow(movement_y, 2))/math.sqrt(math.pow(n2x-n1x, 2) + math.pow(n2y-n1y, 2)))

        x = px + movement*movement_x
        y = py + movement*movement_y
        return (x,y)

    #min und max movement beziehen sich auf die Distanz zwischen den Nachbarpunkten.
    #ein movement von 1 würde bedeuten, dass der Punkt sich um die Länge der Entfernung der Nachbarpunkte zueinander bewegt
    #erst mal nur für das Äußere
    coords = shape.exterior.coords[:-1]
    coords_neg = shape.exterior.coords[:-1]
    random_selection = []
    for i in range(len(coords)):
        if (not shape.move_restrictions[i]) or (type(shape.move_restrictions[i]) is tuple):
            random_selection.append(i)
    choice = random.choice(random_selection)
    if choice == len(coords)-1:
        n2 = 0
    else:
        n2 = choice+1
    n1 = choice - 1

    movement = random.uniform(min_movement, max_movement)
    movement_neg = movement * (-1)
    coords[choice] = move_point(coords[choice], coords[n1], coords[n2], movement, shape.move_restrictions[choice])
    coords_neg[choice] = move_point(coords_neg[choice], coords_neg[n1], coords_neg[n2], movement_neg, shape.move_restrictions[choice])
    s = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    s = even_out_shape(s, 3)
    s_neg = Shape(coords_neg, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    s_neg = even_out_shape(s_neg, 3)
    while (not s.is_valid) or (not s.is_simple) or (not s_neg.is_valid) or (not s_neg.is_simple):
        if movement <= min_movement:
            print('das sollte besser nicht zu oft hintereinander zu sehen sein')
            return change_shape_simple(shape, min_movement, max_movement, n_times)
        else:
            coords = shape.exterior.coords[:-1]
            coords_neg = shape.exterior.coords[:-1]
            movement = movement/2
            movement_neg = movement_neg/2
            coords[choice] = move_point(coords[choice], coords[n1], coords[n2], movement, shape.move_restrictions[choice])
            coords_neg[choice] = move_point(coords_neg[choice], coords_neg[n1], coords_neg[n2], movement_neg, shape.move_restrictions[choice])
            s = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
            s = even_out_shape(s, 3)
            s_neg = Shape(coords_neg, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
            s_neg = even_out_shape(s_neg, 3)
    return random.choice([s, s_neg])
    
#shell - Liste mit tuples (Koordinaten)
#move_restrictions - gleiche länge wie shell
    #Ture - darf sich bewegen 
    #False - darf sich nicht bewegen
    #tuple - Vektor in welche Richtung Punkt sich bewegen darf
#fixed_displacement - gleiche lände wie shell, enthält tuples mit x = True/False und y=True/False
class Shape(geometry.Polygon):
    def __init__(self, shell, holes=None, move_restrictions=None, fixed_displacements=None, forces=None):
        super().__init__(shell, holes)

        if move_restrictions is None:
            self.move_restrictions = [False]*len(shell)
        else:
            self.move_restrictions=move_restrictions

        if fixed_displacements is None:
            self.fixed_displacements = [(False),(False)]*len(shell)
        else:
            self.fixed_displacements=fixed_displacements

        if forces is None:
            self.forces = [(False),(False)]*len(shell)
        else:
            self.forces=forces
            
        
        #einige Methoden und Attribute, die schon da sind:
            
        #object.exterior.coords -> Liste mit äußeren Koordinaten [(x,y),(x,y)...]
        #object.interior.coords -> innere Koordinaten[[(x,y),(x,y)...],[...],...]
        #object.is_valid -> True wenn valid
        #object.is_simple -> True wenn keine Überschneidung mit sich selbst
        #object.area
        #...


if __name__=='__main__':
    pass