import shape
import examples

ex = examples.create_example_polygon()
coords = list(ex.exterior.coords[:-1])
print(coords)
