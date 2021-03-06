from shapely import geometry
import numpy as np
import random
import math
import examples
import csv

def str_to_bool(str_):
    if str_ == 'True':
        return True
    elif str_ == 'False':
        return False
    else:
        return None
def point_perpendicular_at_distance(point, neighbour1, neighbour2, distance):
    """returns a point at a given distance perpendicular to a line given by two other points

    A negative distance, as well as exchanging neighbour1 and neighbour2 will result in
    the calculated point laying on the opposite side of the line
    
    Args:
        neighbour1 (iterable object of length 2): first point defining the line
        neighbour2 (iterable object of length 2): second point defining the line
        distance (float): distance to the initial point
    """

    sx, sy = neighbour1
    ex, ey = neighbour2
    px, py = point

    movement_x = ey - sy
    movement_y = sx - ex

    vec_len = math.sqrt(movement_x**2 + movement_y**2)

    movement_x = (movement_x/vec_len)*distance
    movement_y = (movement_y/vec_len)*distance

    x = px + movement_x
    y = py + movement_y
    return (x,y)


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

def distance(point1,point2):
    """Calculates the distance between two points in the cartesian coordinate system
    
    Args:
        point1 ((float,float)): Point 1
        point2 ((float,float)): Point 2
    
    Returns:
        float: Distance between Point 1 and Point 2
    """
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

def shortest_line(shape,data_type):
    lines = get_lines(shape)
    shortest_line = None
    for line in lines:
        if  shortest_line == None or distance(line[0],line[1])<shortest_line:
            if data_type == 'v':
                shortest_line = distance(line[0],line[1])
            elif data_type == 'l':
                shortest_line = line
    return shortest_line
        
def line_intersection(line1, line2): 
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0]) 
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

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
            return [distance(point,s),None]
        else:
            return [min(distance(point,line[0]),distance(point,line[1])),line]
        
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
        
def point_between_points(point1,point2,factor=0.5):
    """Creates a point located on a line between two points in the cartesian coordinate system
    
    Args:
        point1 ((float,float)): Point 1
        point2 ((float,float)): Point 2
        factor (float, optional): Determines where the new point is located. If 0 the new point equals Point 1,
        if 0.5 the new point is in the middle between Point 1 and Point 2
        and if 1 the point equals Point2. Defaults to 0.5.
    
    Returns:
        ((float,float)): Point between Point 1 and Point 2
    """
    x1,y1 = point1
    x2,y2 = point2
    x = ((x2-x1)*factor)+x1
    y = ((y2-y1)*factor)+y1
    return x,y



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

def change_shape_two(shape, min_movement=0.1, max_movement=1):
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

    def linear_function(shape,coords_change):
        ### Lineare Funktion ###
        coords = shape.exterior.coords[:-1]
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
        return Shape(coords, shape.interiors, shape.move_restrictions, shape.fixed_displacements, shape.forces)

    ### Zu ändernde Koordinaten werden bestimmt ###
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
    
    ### Umformung ###
    s = linear_function(shape,coords_change)

    ### Kontrollen ###
    while not(s.is_valid) or not(s.is_simple) or not(s.is_thick()):
        s = change_shape_two(shape)

    ### Glätten ###
    s = even_out_shape(s, 3)
    return s

def csv_to_shape(file_path):
    with open(file_path,'r') as file:
        csv_reader = csv.reader(file)
        coords = []
        forces = []
        move_restrictions = []
        fixed_displacements = []
        next(csv_reader,None)
        for line in csv_reader:
            coords.append((float(line[0]),float(line[1])))
            forces.append((float(line[2]),float(line[3])))
            move_restrictions.append((not str_to_bool(line[4]),not str_to_bool(line[5])))
            fixed_displacements.append(( str_to_bool(line[4]), str_to_bool(line[5])))
        return Shape(coords,None,move_restrictions,fixed_displacements,forces)

def imagej_to_shape(file_path):
    with open(file_path,'r') as file:
        csv_reader = csv.reader(file)
        coords = []
        next(csv_reader,None)
        for line in csv_reader:
            coords.append((float(line[5]),float(line[6])))
        return Shape(coords,None,None,None,None)




    
#shell - Liste mit tuples (Koordinaten)
#move_restrictions - gleiche länge wie shell
    #True - darf sich bewegen 
    #False - darf sich nicht bewegen
    #tuple - Vektor in welche Richtung Punkt sich bewegen darf
#fixed_displacement - gleiche lände wie shell, enthält tuples mit x = True/False und y=True/False
class Shape(geometry.Polygon):
    def __init__(self, shell, holes=None, move_restrictions=None, fixed_displacements=None, forces=None):
        super().__init__(shell, holes)

        if move_restrictions is None:
            self.move_restrictions = [False]*len(shell)
        else:
            new_move_restrictions = []
            for move_restriction in move_restrictions:
                if isinstance(move_restriction,tuple) and  move_restriction[0] and  move_restriction[1]:
                    new_move_restrictions.append(False)
                elif isinstance(move_restriction,tuple) and  not move_restriction[0] and  not move_restriction[1]:
                    new_move_restrictions.append(True)
                else:
                    new_move_restrictions.append(move_restriction)
            self.move_restrictions=new_move_restrictions

        if fixed_displacements is None:
            self.fixed_displacements = [(False,False)]*len(shell)
        else:
            self.fixed_displacements=fixed_displacements

        if forces is None:
            self.forces = [(False,False)]*len(shell)
        else:
            self.forces=forces

        self.fittness = None

    def is_thick(self,factor=1):   
        limit = shortest_line(self,'v')*factor
        for point in self.exterior.coords[:-1]:
            if smallest_distance_point_shape(point,self,True)[0] < limit:
                return False
        return True

    def check_shape(self):
        if not self.is_valid or not self.is_simple:
            return False
        else:
            return True
            
        
        #einige Methoden und Attribute, die schon da sind:
            
        #object.exterior.coords -> Liste mit äußeren Koordinaten [(x,y),(x,y)...]
        #object.interior.coords -> innere Koordinaten[[(x,y),(x,y)...],[...],...]
        #object.is_valid -> True wenn valid
        #object.is_simple -> True wenn keine Überschneidung mit sich selbst
        #object.area
        #...


if __name__=='__main__':
    pass
