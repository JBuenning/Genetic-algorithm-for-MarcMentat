import shapely.geometry as geometry
import shape
import matplotlib.pyplot as plt

coords = [(0,0),(1,0),(1,1),(0,1)]
a = shape.Shape(coords)
b = geometry.LineString(coords)

print(shape.get_lines(coords))
# print(list(a.exterior.coords))

# plt.plot(*a.exterior.xy)
# plt.show()

# print(isinstance(coords,list))