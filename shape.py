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
def get_cool_example():
    shell = [(0,8),(0,9),(0,10),(0,11),(0,12),(0,13),(0,14),(0,15),(0,16),(1,16),(2,16),(2,15),
            (2,14),(3,14),(4,14),(5,14),(6,14),(6,15),(6,16),(7,16),(8,16),(8,15),(8,14),
            (9,14),(10,14),(11,14),(12,14),(13,14),(14,14),(14,15),(14,16),(15,16),(16,16),(16,15),
            (16,14),(17,14),(18,14),(19,14),(20,14),(20,15),(20,16),(21,16),(22,16),
            (22,15),(22,14),(22,13),(22,12),(22,11),(22,10),(22,9),(22,8),
            (21,8),(20,8),(19,8),(18,8),(17,8),(16,8),(15,7),(14,6),
            (14,5),(14,4),(14,3),(14,2),(14,1),(14,0),(13,0),(12,0),(11,0),(10,0),(9,0),(8,0),
            (8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(7,7),(6,8),(5,8),(4,8),(3,8),(2,8),(1,8)]
    move_restrictions = [False,False,False,False,False,False,False,False,
                        True,True,True,
                        False,False,False,False,False,False,False,
                        True,True,True,
                        False,False,False,False,False,False,False,False,False,
                        True,True,True,
                        False,False,False,False,False,False,False,
                        True,True,True,
                        False,False,False,False,False,False,False,False,
                        False,False,False,False,False,False,False,False,False,False,False,False,False,
                        True,True,True,True,True,True,True,
                        False,False,False,False,False,False,False,False,False,False,False,False,False]
    return Shape(shell, move_restrictions=move_restrictions)

def get_distance(point1,point2):
    x1,y1 = point1
    x2,y2 = point2
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(math.pow(dx,2)+math.pow(dy,2))

def get_lines(shape):
    coords = shape.exterior.coords[:-1]
    lines = []
    for i in range(1,len(coords)):
        lines.append([coords[i-1],coords[i]])
    lines.append([coords[len(coords)-1],coords[0]])
    return lines

def line_intersection(line1, line2): 
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0]) 
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here 

    def det(a, b): 
     return a[0] * b[1] - a[1] * b[0] 

    div = det(xdiff, ydiff) 
    if div == 0: 
     raise Exception('lines do not intersect') 

    d = (det(*line1), det(*line2)) 
    x = det(d, xdiff)/div 
    y = det(d, ydiff)/div 
    return x, y 

def smallest_distance_point_shape(point,shape,point_in_shape):
    def smallest_distance_point_line(point,line):
        x1,y1=line[0]
        x2,y2=line[1]
        px1,py1=point
        m1=(x2-x1,y2-y1)
        m2=(m1[1],-m1[0])
        px2=px1+m2[0]
        py2=py1+m2[1]
        s = line_intersection(line,[point,(px2,py2)])
        try:
            t=(s[0]-x1)/m1[0]
        except:
            t=(s[1]-y1)/m1[1]
        if t<=1 and t>=0:
            return [get_distance(point,s),None]
        else:
            return [min(get_distance(point,line[0]),get_distance(point,line[1])),line]
        
    coords = shape.exterior.coords[:-1]
    lines = get_lines(shape)
    smallest_distance= None
    
    for line in lines:
        if point_in_shape:
            if point in line:
                continue
        if smallest_distance==None or smallest_distance_point_line(point,line)[0] < smallest_distance[0]:
            smallest_distance = smallest_distance_point_line(point,line)
    
    if point_in_shape and smallest_distance[1] != None: #gar nicht schön gelöst aber wichtig 
        n1 = coords[coords.index(point)-1]
        if coords.index(point) == len(coords)-1:
            n2 = coords[0]
        else:
            n2 = coords[coords.index(point)+1]
        if n1 in smallest_distance[1] or n2 in smallest_distance[1]: #nicht die schönste Lösung
            return [smallest_distance[0],True]#True - kürzeste Distanz liegt auf der Umrandung des Polygons
    return [smallest_distance[0],False]#False - kürzeste Distanz liegt nicht auf der Umrandung des Polygons
        
#Algorithmus macht ähnliche Abstände zwischen Punkten und rundet die Form dabei ab. Die Fläche wird dabei kleiner
#jeder Puktk wird dabei genau zwischen seine beiden Nachbarpunkte verschoben
#glicht noch nicht die Interiors aus
#teilweise beschränkte Bewegung fehlt noch
#es wird nicht überprüft, ob die Shape, die zurückgegeben wird, zulässig ist
def round_shape(shape, n_times=1):
    def round_point(point, neighbour1, neighbour2, restriction):
        if restriction:
            if type(restriction) is tuple:
                raise NotImplementedError('partially restricted movement not supported yet')
            else:
                return point
        else:
            n1x, n1y = neighbour1
            n2x, n2y = neighbour2
            mx = (n2x + n1x)/2
            my = (n2y + n1y)/2
            return (mx, my)

    coords = shape.exterior.coords[:-1]
    indices = list(range(len(coords)))
    random.shuffle(indices)
    for j in indices:
        coords[j-1] = round_point(coords[j-1], coords[j], coords[j-2], shape.move_restrictions[j-1])
        shape = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    if n_times == 1:
        return shape
    else:
        return round_shape(shape, n_times - 1)

#n_times - wie oft soll der algorithmus laufen
#Algorithmus macht ähnliche Abstände zwischen Punkten ohne Fläche und Form stark zu verändern
#es wird nicht überprüft, ob die Shape, die zurückgegeben wird, zulässig ist
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
                    t,_ = np.linalg.solve(A,B)

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
            t,_ = np.linalg.solve(A,B)

            x = px + t*(n2x - n1x)
            y = py + t*(n2y - n1y)
        return(x,y)
    #bisher nur äussere form
    coords = shape.exterior.coords[:-1]
    indices = list(range(len(coords)))
    random.shuffle(indices)
    for i in indices:
        coords[i-1] = even_out_point(coords[i-1], coords[i], coords[i-2], shape.move_restrictions[i-1])

    shape = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    if n_times == 1:
        return shape
    else:
        return even_out_shape(shape, n_times - 1)
    
#ähnlicher Algorithmus wie change_shape_one. Der Unterschied ist, das dieser Algorithmus die Tendenz hat, dünne Strukturen zu vermeiden.
#Daher wird die Fläche der Form tendentiell größer
#zusätzlich: round shape, wenn eine bestimmte reursion depth erreicht ist
def change_shape_three(shape, min_movement=0.1, max_movement=1, max_recursiondepth=4, endless_loop_counter=0):
    def move_point(point, neighbour1, neighbour2, movement, restriction):#ist die gleiche Funktion wie bei change_shape_one
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

    coords = shape.exterior.coords[:-1]
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
    movement = movement * random.choice([1, -1])
    coords[choice] = move_point(coords[choice], coords[n1], coords[n2], movement, shape.move_restrictions[choice])
    s = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    s = even_out_shape(s, 3)
    while (not s.is_valid) or (not s.is_simple):
        
        if movement <= min_movement:
            if endless_loop_counter >= max_recursiondepth:
                print('round shape')
                return change_shape_three(round_shape(shape), min_movement, max_movement, max_recursiondepth, 0)
            else:

                print('das sollte besser nicht zu oft hintereinander zu sehen sein')
                return change_shape_three(shape, min_movement, max_movement, max_recursiondepth, endless_loop_counter+1)
        else:
            coords = shape.exterior.coords[:-1]
            movement = movement/2
            coords[choice] = move_point(coords[choice], coords[n1], coords[n2], movement, shape.move_restrictions[choice])
            s = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
            s = even_out_shape(s, 3)
    return s


#zufällige Form
#max_movement - in prozent bezogen auf abstand beider nachbarpunkte zueinander
#min_movement - siehe max
def change_shape_one(shape, min_movement=0.1, max_movement=1, max_recursiondepth=20, endless_loop_counter=0):
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
    #s = round_shape(s, 1)
    s_neg = Shape(coords_neg, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
    s_neg = even_out_shape(s_neg, 3)
    #s_neg =round_shape(s_neg, 1)
    while (not s.is_valid) or (not s.is_simple) or (not s_neg.is_valid) or (not s_neg.is_simple):
        if movement <= min_movement:
            if endless_loop_counter >= max_recursiondepth:
                print('round shape')
                return change_shape_one(round_shape(shape), min_movement, max_movement, max_recursiondepth, 0)
            else:
                print('das sollte besser nicht zu oft hintereinander zu sehen sein')
                return change_shape_one(shape, min_movement, max_movement, max_recursiondepth, endless_loop_counter+1)

        else:
            coords = shape.exterior.coords[:-1]
            coords_neg = shape.exterior.coords[:-1]
            movement = movement/2
            movement_neg = movement_neg/2
            coords[choice] = move_point(coords[choice], coords[n1], coords[n2], movement, shape.move_restrictions[choice])
            coords_neg[choice] = move_point(coords_neg[choice], coords_neg[n1], coords_neg[n2], movement_neg, shape.move_restrictions[choice])
            s = Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
            s = even_out_shape(s, 3)
            #s = round_shape(s, 1)
            s_neg = Shape(coords_neg, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)
            s_neg = even_out_shape(s_neg, 3)
            #s_neg =round_shape(s_neg, 1)
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
