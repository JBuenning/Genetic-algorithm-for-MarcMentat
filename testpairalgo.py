from shapely import geometry
import tkinter as tk
import time
import examples
from algorithms import mutation_algorithms
import core
import matplotlib.pyplot as plt
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


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
        coords_intersection = intersection.exterior.coords[:-1]
        shps = [shp1,shp2]
        blub = []
        for i,shp in enumerate(shps):
            other_shp = shps[int(not bool(i))]
            coords = shp.exterior.coords[:-1]
            diffs = []
            i=0
            while i < len(coords):
                if not coords[i] in intersection.exterior.coords:
                    j=coords_intersection.index(coords[i-1])
                    if not coords_intersection[j+1] in other_shp.exterior.coords:
                        j+=1
                    outer_coords = [coords_intersection[j]]
                    inner_coords = [coords_intersection[j]]
                    j+=1
                    while coords_intersection[j] not in coords:
                        inner_coords.append(coords_intersection[j])
                        j+=1


                    outer_coords.append(coords[i])
                    i+=1
                    while not coords[i] in intersection.exterior.coords:
                        outer_coords.append(coords[i])
                        i+=1

                    if inner_coords[-1] not in other_shp.exterior.coords and len(inner_coords) > 1:
                        outer_coords.append(inner_coords[-1])
                    elif coords_intersection[j] in other_shp.exterior.coords and coords_intersection[j] in coords:
                        inner_coords.append(coords_intersection[j])
                        outer_coords.append(coords_intersection[j])


                    diffs.append((inner_coords,outer_coords))
                else:
                    i+=1
            blub.extend(diffs)
        return blub
                





plt.plot(*p1.exterior.xy, marker = 'o',color='yellow',alpha = 0.5)
plt.plot(*p2.exterior.xy, marker = 'o',color='blue',alpha = 0.5)
# # plt.show()
x = pair_shapes(p1,p2)
print(x)
for b in x:
    plt.plot(*zip(*b[0]),color='black',marker='o')
    plt.plot(*zip(*b[1]),color='red',marker='o')
# print(x)
# for l in x:
#     # f = geometry.LineString(l)
#     plt.plot(*l.exterior.xy, marker = 'o',color='red')
plt.show()