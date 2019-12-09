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

def pair_shapes(shp1, shp2):
    def pair_two_sections(sections):
        section=None
        return sections

    shps = [shp1,shp2]
    all_sections = []
    shared_part = []
    for i,shp in enumerate(shps):
        other_shp = shps[int(not bool(i))]
        diff = shp.difference(other_shp)
        if type(diff) == geometry.polygon.Polygon:
            diffs = [diff]
        else:
            diffs = list(diff)

        for diff in diffs:
            diff_coords = diff.exterior.coords[:-1]
            crossing_coords = []
            for coord in diff_coords:
                if coord not in shp1.exterior.coords and coord not in shp2.exterior.coords:
                    crossing_coords.append(coord)
                elif coord in shp1.exterior.coords and coord in shp2.exterior.coords:
                    crossing_coords.append(coord)
            if len(crossing_coords) != 2:
                print('If this is printed out most likely one of the lines of one shape happens to go directly through the point of th other shape without having a point there itself. There is no solution for this case. Yet!')
                return
            coords_splitted = [[],[]]# better as tuple?
            i=diff_coords.index(crossing_coords[0])
            j=0
            first_cycle = True
            while True:
                coords_splitted[j].append(diff_coords[i])
                if diff_coords[i] == crossing_coords[1]:
                    j=1
                    coords_splitted[j].append(diff_coords[i])
                elif not first_cycle and diff_coords[i] == crossing_coords[0]:
                    break
                if i == len(diff_coords)-1:
                    i=0
                else:
                    i+=1
                first_cycle = False
            coords_splitted[1].reverse()
            section = pair_two_sections(coords_splitted)
            all_sections.append(section)
    
    # join all sections
    middle_way = []
    return all_sections

# plt.plot(*p1.exterior.xy,color='blue')
# plt.plot(*p2.exterior.xy,color='yellow')

a = pair_shapes(p1,p2)


for b in a:
    print(b)
    plt.plot(*p1.exterior.xy,color='blue',marker='o')
    plt.plot(*p2.exterior.xy,color='yellow',marker='o')
    plt.plot(*zip(*b[0]),color='black',marker='x')
    plt.plot(*zip(*b[1]),color='red',marker='x')
    plt.show()