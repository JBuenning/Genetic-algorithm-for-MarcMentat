import shape
import matplotlib.pyplot as plt

p1 = shape.Shape([(0,0),(0,1.5),(0,2),(0,3),(0,4),(1,4),(2,4),(2,3),(1,3),(1,2),(1,1),(2,1),(3,1),(3,0),(2,0),(1,0)])
p2 = shape.Shape([(0,0),(0,1),(0,2.5),(0,3),(0,4),(1,4),(1,3),(1,2),(1,1),(2,1),(2,2),(3,2),(3,1),(3,0),(2,0),(1,0)])

def pair_shapes(shp1, shp2):
        coords_new = []
        if len(shp1.exterior.coords) == len(shp1.exterior.coords):
            coords_num = len(shp1.exterior.coords)-1
        else:
            print('Fehler')

        shp1_l = shp1.length/coords_num
        shp2_l = shp2.length/coords_num

        shp1_lines = shape.get_lines(shp1)
        shp2_lines = shape.get_lines(shp2)

        shp1_coords_compare = []
        shp2_coords_compare = []

        i = 0
        left = 0
        print(shp1_lines)
        print(len(shp1_lines))
        print(coords_num)
        for j in range(coords_num):
            print(j)
            print(i)
            print('')
            distance = shape.get_distance(shp1_lines[i][0],shp1_lines[i][1])
            if distance+left > shp1_l:
                distance_on_line = shp1_l-left
                prozent = distance_on_line/distance
                point = shape.point_between_points(shp1_lines[i][0],shp1_lines[i][1],prozent)
                shp1_coords_compare.append(point)
                left = distance-distance_on_line
                if left < shp1_l:
                    i+=1
                elif left > shp1_l:
                    left = -distance_on_line
                elif left == shp1_l:
                    shp1_coords_compare.append(shp1_lines[i][1])
                    left = 0
                    i +=1
            elif distance+left <shp1_l:
                left = left+distance
                i+=1
            elif distance+left == shp1_l:
                shp1_coords_compare.append(shp1_lines[i][1])
                left=0
                i+=1
        return shape.Shape(shp1_coords_compare)

p=pair_shapes(p1,p2)
plt.plot(*p.exterior.xy, marker = 'o')
plt.show()
