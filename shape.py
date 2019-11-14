from shapely import geometry
import matplotlib.pyplot as plt
import numpy as np
import random
import math

def even_out_point(point, neighbour1, neighbour2, restriction=False):
    #hilfsfunktion für even_out_shape
    px, py = point
    n1x, n1y = neighbour1
    n2x, n2y = neighbour2
    mx = (n2x + n1x)/2#mitte zwischen den Nachbarpunkten
    my = (n2y + n1y)/2
    
    if restriction:
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
        #in Matrixschreibweise AX=B
        A = np.array([[n2x-n1x, n1y-n2y],[n2y-n1y, n2x-n1x]])
        B = np.array([mx-px, my-py])
        t,u = np.linalg.solve(A,B)

        x = px + t*(n2x - n1x)
        y = py + t*(n2y - n1y)
    return(x,y)

def even_out_shape(shape, n_times=1):
    #bisher nur äussere form
    coords = shape.exterior.coords[:-1]
    for i in range(len(coords)):
        coords[i-1] = even_out_point(coords[i-1], coords[i], coords[i-2])

    shape = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    if n_times == 1:
        return shape
    else:
        return even_out_shape(shape, n_times - 1)

def move_point(point, neighbour1, neighbour2, movement, restriction):
    #Hilfsfuntion für change_shape
    n1x, n1y = neighbour1
    n2x, n2y = neighbour2
    px, py = point
    if restriction:
        movement_x, movement_Y = restriction
    else:
        movement_x = n2y - n1y
        movement_y = n1x - n2x

    movement = movement * (math.sqrt(math.pow(movement_x, 2) + math.pow(movement_y, 2))/math.sqrt(math.pow(n2x-n1x, 2) + math.pow(n2y-n1y, 2)))

    x = px + movement*movement_x
    y = py + movement*movement_y

    return (x,y)

    

def change_shape_simple(shape, min_movement=0.1, max_movement=1, n_times=1):
    #min und max movement beziehen sich auf die Distanz zwischen den Nachbarpunkten.
    #ein movement von 1 würde bedeuten, dass der Punkt sich um die Länge der Entfernung der Nachbarpunkte zueinander bewegt
    #erst mal nur für das Äußere
    coords = shape.exterior.coords[:-1]
    n2 = random.randrange(len(coords))
    choice = n2 - 1
    n1 = n2 - 2

    #mögliches Problem: Form wird größer, weil Überschneidung unwahrscheinlicher
    movement = random.uniform(min_movement, max_movement)
    movement = movement * random.choice([1,-1])
    coords[choice] = move_point(coords[choice], coords[n1], coords[n2], movement, shape.move_restrictions[choice])
    shape = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    shape = even_out_shape(shape, 2)
    print('noch keine Validierung, es können auch unzulässige Formen entstehen')
    return shape #noch keine Validierung
    
    
    
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
















