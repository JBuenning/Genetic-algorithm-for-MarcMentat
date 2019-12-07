import shapely.geometry as geometry

a = geometry.Polygon([(0,0),(0,1),(1,1),(1,0)])

b = geometry.Point(0,0)

print(a.contains(b))