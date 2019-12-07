import shape
import matplotlib.pyplot as plt

p1 = shape.Shape([(0,0),(0,1.5),(0,2),(0,3),(0,4),(1,4),(2,4),(2,3),(1,3),(1,2),(1,1),(2,1),(3,1),(3,0),(2,0),(1,0)])
p2 = shape.Shape([(0,0),(0,1),(0,2.5),(0,3),(0,4),(1,4),(1,3),(1,2),(1,1),(2,1),(2,2),(3,2),(3,1),(3,0),(2,0),(1,0)])

def pair_shapes(shp1, shp2,coords_num):
    def get_even_spreaded_points(shp,coords_num):
        shp_coords_compare = []
        shp_l = shp.length/coords_num
        shp_lines = shape.get_lines(shp)
        i = 0
        left = 0
        while i < len(shp_lines):
            distance = shape.get_distance(shp_lines[i][0],shp_lines[i][1])
            if distance+left > shp_l:
                distance_on_line = shp_l-left
                prozent = distance_on_line/distance
                point = shape.point_between_points(shp_lines[i][0],shp_lines[i][1],prozent)
                shp_coords_compare.append(point)
                left = distance-distance_on_line
                if left < shp_l:
                    i+=1
                elif left > shp_l:
                    left = -distance_on_line
                elif left == shp_l:
                    shp_coords_compare.append(shp_lines[i][1])
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

    coords_new = []
    if len(shp1.exterior.coords) == len(shp1.exterior.coords):
        # coords_num = len(shp1.exterior.coords)-1
        coords_num = coords_num
    else:#hier irgendwo coord_num überprüfen - darf nicht 1 oder 2 sein
        print('Fehler')

    coords_compare = []
    coords_compare.append(get_even_spreaded_points(shp1,coords_num))
    coords_compare.append(get_even_spreaded_points(shp2,coords_num))
    k1  = coords_compare[0]
    k2 = coords_compare[1]


    for i in range(coords_num):
        point = shape.point_between_points(coords_compare[0][i],coords_compare[1][i])
        coords_new.append(point)
    
    return [shape.Shape(coords_new),shape.Shape(k1),shape.Shape(k2)]
string= ''
for i in range(100):
    try:
        pair_shapes(p1,p2,i)
    except:
        string += '{}, '.format(i)
print(string)
array=pair_shapes(p1,p2,i)
p=array[0]
k1=array[1]
k2=array[2]
plt.plot(*p1.exterior.xy, marker = 'o')
plt.plot(*p2.exterior.xy, marker = 'o',color='yellow')
plt.plot(*k1.exterior.xy, marker = 'o',color='green')
plt.plot(*k2.exterior.xy, marker = 'o',color='orange')
plt.plot(*p.exterior.xy,marker = 'o',color='red')
plt.show()
