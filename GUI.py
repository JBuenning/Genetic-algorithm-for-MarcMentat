import tkinter as tk
import matplotlib.pyplot as plt
##import shapely
##from shapely.geometry import Polygon
from shape import Shape

### Initalisieren des Fensters ###


##root = tk.Tk()
##frame = tk.Frame(root, bg = 'black')
##canvas = tk.Canvas(root, height=500, width=500)
##canvas.pack()

def show_polygon():
    pass

def create_example_polygon():
    return Shape([(0,0),(2,2),(2,1),(1,0)],[[(1,1), (1,2), (2,1)]])

example = create_example_polygon()

plt.plot(*example.exterior.xy, marker = 'o')
plt.show()

#root.mainloop()
