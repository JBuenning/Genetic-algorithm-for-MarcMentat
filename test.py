import shapely.geometry as geometry
import shape
import matplotlib.pyplot as plt


a = geometry.LineString([(0,0),(0,2)])
c = shape.Shape([(0,0),(0,1),(1,1),(1,0)])

b = shape.get_even_spreaded_points(a,3)

plt.plot(*a.xy,color='red',marker='o')
plt.plot(*zip(*b),color='blue',marker='o')
plt.show()

print(b)