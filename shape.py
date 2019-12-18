from shapely import geometry
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import examples

    
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
            self.fixed_displacements = [(False,False)]*len(shell)
        else:
            self.fixed_displacements=fixed_displacements

        if forces is None:
            self.forces = [(False,False)]*len(shell)
        else:
            self.forces=forces

    def is_thick(self,factor=1):   
        limit = shortest_line(self,'v')*factor
        for point in self.exterior.coords[:-1]:
            if smallest_distance_point_shape(point,self,True)[0] < limit:
                return False
        return True
        
        
        #einige Methoden und Attribute, die schon da sind:
            
        #object.exterior.coords -> Liste mit äußeren Koordinaten [(x,y),(x,y)...]
        #object.interior.coords -> innere Koordinaten[[(x,y),(x,y)...],[...],...]
        #object.is_valid -> True wenn valid
        #object.is_simple -> True wenn keine Überschneidung mit sich selbst
        #object.area
        #...

def get_even_spreaded_points(obj,*args):
        if type(obj) == list:
            shp = geometry.LineString(obj)
        # elif type(obj) !=  geometry.LineString and type(obj) != shape: #Fehler bei shape
            # print('get_even_spreaded_points called with not suitable object')
        else:#notlösung
            shp = obj
            coords_num = -1

        shp_coords_compare = []
        
        shp_lines = get_lines(shp) # anpassen was passiert wenn shp linestring ist- methode anpassen
        
        if args:
            coords_num=args[0]
        else:
            coords_num+=len(shp_lines)+1

        if type(obj)==geometry.LineString:
            shp_l = shp.length/(coords_num-1)
            shp_coords_compare.append(shp_lines[0][0])
        else:#notlösung
            shp_l = shp.length/coords_num
        i = 0
        left = 0
        for _ in range(coords_num):
            distance = get_distance(shp_lines[i][0],shp_lines[i][1])# hier muss umgebaut werden vllt die for zur while shleife machen und immer wieder i kontrollieren
            if distance+left > shp_l:
                distance_on_line = shp_l-left
                prozent = distance_on_line/distance
                point = point_between_points(shp_lines[i][0],shp_lines[i][1],prozent)
                shp_coords_compare.append(point)
                left = distance-distance_on_line
                left = round(left,15)
                if left < shp_l:
                    if i == len(shp_lines)-1:#eher notlösung
                        shp_coords_compare.append(shp_lines[i][1])
                        break
                    i+=1
                elif left > shp_l:
                    left = -distance_on_line
                elif left == shp_l:
                    shp_coords_compare.append(shp_lines[i][1])
                    if i == len(shp_lines)-1:
                        break
                    left = 0
                    i +=1
            elif distance+left <shp_l:
                left = left+distance
                i+=1
            elif distance+left == shp_l:
                shp_coords_compare.append(shp_lines[i][1])
                left=0
                i+=1
        return shp_coords_compare

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

def get_distance(point1,point2):
    x1,y1 = point1
    x2,y2 = point2
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(math.pow(dx,2)+math.pow(dy,2))

def get_lines(obj):
    """Returns all the the lines of an object that represents a geometry
    
    Args:
        obj (list,LineString,Polygon or Shape): Must contain exterior coordinates
    
    Returns:
        list: A list of tuples that represent coordinates
    """
    if isinstance(obj,geometry.LineString):
        coords = list(obj.coords)
    elif isinstance(obj,Shape) or isinstance(obj,geometry.Polygon):
        coords = list(obj.exterior.coords)
    elif isinstance(obj,list):
        coords = obj

    lines = []
    for i in range(1,len(coords)):
        lines.append([coords[i-1],coords[i]])

    return lines

def shortest_line(shape,data_type):#data_type - l gibt line zurück, v den wert
    lines = get_lines(shape)
    shortest_line = None
    for line in lines:
        if  shortest_line == None or get_distance(line[0],line[1])<shortest_line:
            if data_type == 'v':
                shortest_line = get_distance(line[0],line[1])
            elif data_type == 'l':
                shortest_line = line
    return shortest_line
        
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
        
def point_between_points(point1,point2,factor=0.5):#factor- 0.5 entspricht dem mittel
    x1,y1 = point1
    x2,y2 = point2
    x = ((x2-x1)*factor)+x1
    y = ((y2-y1)*factor)+y1
    return (x,y)


def join_shapes(shape1,shape2):
    random_range = 0.2

    coords1 = shape1.exterior.coords[:-1]
    coords2 = shape2.exterior.coords[:-1]
    coords = [coords1,coords2]
    if len(coords1) != len(coords2):
        print('Achtung ganz böse Ausnahme hier fehlt noch etwas Programmierarbeit um beide Listen auf die gleich eLänge zu bringen')
    
    if False:
        start_points = []
        smallest_distance = 9999999
        for point1 in coords1:
            for point2 in coords2:
                if get_distance(point1,point2) < smallest_distance:
                    smallest_distance = get_distance(point1,point2)
                    start_points = [point1,point2]
        coords_sorted = []
        for i in range(2):
            array = []
            j = coords[i].index(start_points[i])
            while j < len(coords[i]):
                array.append(coords[i][j])
                j += 1
            for point in coords[i]:
                if point == start_points[i]:
                    break
                else:
                    array.append(point)
            coords_sorted.append(array)
        coords1,coords2 = coords_sorted

    coords_new = []
    for i in range(len(coords1)):
        coords_new.append(point_between_points(coords1[i],coords2[i],0.5))
    ### Hier muss noch überprüft werden ob denn restrictions usw bei beidne shapes übereinstimmen
    return Shape(coords_new, shape1.interiors, shape1.move_restrictions, shape1.fixed_displacements, shape1.forces)


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



if __name__=='__main__':
    pass