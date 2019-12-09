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
        all_diffs = []
        for i,shp in enumerate(shps):
            other_shp = shps[int(not bool(i))]
            diff = shp.difference(other_shp)
            if type(diff) == geometry.polygon.Polygon:
                diffs = [diff]
            else:
                diffs = list(diff)
            all_diffs.extend(diffs)
        return all_diffs

# plt.plot(*p1.exterior.xy,color='blue')
# plt.plot(*p2.exterior.xy,color='yellow')

a = pair_shapes(p1,p2)

intersection = p1.intersection(p2)
i_coords = intersection.exterior.coords[:-1]
keruzpunkte = []
for coord in i_coords:
    if coord not in p1.exterior.coords and coord not in p2.exterior.coords:
        keruzpunkte.append(coord)

for b in a:
    print(b.exterior.coords)
    print(len(b.exterior.coords))
    plt.plot(*p1.exterior.xy,color='blue',marker='o')
    plt.plot(*p2.exterior.xy,color='yellow',marker='o')
    plt.plot(*b.exterior.xy,color='black',marker='x')
    plt.scatter(*zip(*keruzpunkte),marker='o',color='red')
    plt.show()