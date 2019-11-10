from shapely import geometry
import matplotlib.pyplot as plt

class Shape(geometry.Polygon):
    def __init__(self, shell, holes=None, fixed_x=None, fixed_y=None):
        super().__init__(shell, holes)
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y #Liste mit Positionen von Punkten, die nicht in x oder y richtung bewegt werden dürfen
        

        #einige Methoden und Attribute, die schon da sind:
            
        #object.exterior.coords -> Liste mit äußeren Koordinaten [(x,y),(x,y)...]
        #object.interior.coords -> innere Koordinaten[[(x,y),(x,y)...],[...],...]
        #object.is_valid -> True wenn valid
        #object.is_simple -> True wenn keine Überschneidung mit sich selbst
        #object.area
        #...
    
def display_shape(shape):
    outer_x, outer_y = shape.exterior.xy
    inner = shape.interiors
    plt.fill(outer_x, outer_y)
    for shape in inner:
        x, y = shape.xy
        plt.fill(x,y, color = 'w')
    plt.show()

s = Shape([(0, 0), (2,8), (10, 10), (10, 0)],[[(1,1), (1,2), (2,1)]])
display_shape(s)
