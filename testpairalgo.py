from shapely import geometry
import tkinter as tk
import time
import examples
from algorithms import mutation_algorithms
import core
import matplotlib.pyplot as plt
p1 = geometry.Polygon([(0,0),(0,1),(0,2),(0,3),(0,4),(0.5,4),(1.5,4),(2,4),(2,3),(1,3),(1,2),(1,1),(2,1),(3,1),(3,0),(2,0),(1,0)])
p2 = geometry.Polygon([(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,5),(1,3),(1,2),(1,1),(2,1),(2,2),(3,2),(3,1),(3,0),(2,0),(1,0)])
e =p1.intersection(p2)
i = p2.difference(e)
c=core.Core()
c.inital_shape=examples.get_realisticreate_example_polygonc_example()
c.generate_first_generation()
p1= c.generations[0][0]
p2= c.generations[0][1]
### Initalisieren des Fensters ###
def pair_shapes(shp1, shp2):
        intersection = shp1.intersection(shp2)
        shps = [shp1,shp2]
        bla = []
        for i,shp in enumerate(shps):
            other_shp = shps[int(not bool(i))]
            diff = shp.difference(intersection)
            if type(diff) == geometry.polygon.Polygon:
                diffs = [diff]
            else:
                diffs = list(diff)
            new_diffs = []
            for diff in diffs:
                new_coords = []
                for coord in diff.exterior.coords[:-1]:
                    if not other_shp.contains(geometry.Point(coord)):
                        new_coords.append(coord)
                print(new_coords)
                try:
                    new_diffs.append(geometry.Polygon(new_coords))
                except:
                    pass
                print(diff)
                print('')
            inner_points =  []
            outer_points = []
        farben=['green','red','blue','orange','pink','yellow','pruple','cyan','magenta']
        for i,l in enumerate(diffs):
            # f = geometry.LineString(l)
            plt.plot(*l.exterior.xy, marker = 'o',color=farben[i])
        for l in new_diffs:
            # f = geometry.LineString(l)
            plt.plot(*l.exterior.xy, marker = 'o',color='black')
        return diff
        #     for polygon in diff:
        #         array = []
        #         for point in polygon.exterior.coords[:-1]:
        #             if point in intersection.exterior.coords[:-1]:
        #                 array.append(point)
        #         inner_points.append(array)
        # return inner_points
plt.plot(*p1.exterior.xy, marker = 'o',color='yellow')
plt.plot(*p2.exterior.xy, marker = 'o',color='blue')
# plt.show()
x = pair_shapes(p1,p2)
# print(x)
# for l in x:
#     # f = geometry.LineString(l)
#     plt.plot(*l.exterior.xy, marker = 'o',color='red')
plt.show()