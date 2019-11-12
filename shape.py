from shapely import geometry
import matplotlib.pyplot as plt

class Shape(geometry.Polygon):
    def __init__(self, shell, holes=None, fixed_x=None, fixed_y=None):
        super().__init__(shell, holes)
        
        if fixed_x is None:
            self.fixed_x = [False]*(len(shell)+1)#möglicher Konflikt, wenn erster Punkt doppelt genannt wird!!!
        else:
            self.fixed_x = fixed_x

        if fixed_y is None:
            self.fixed_y = [False]*(len(shell)+1)
        else:
            self.fixed_y = fixed_y


        #fixed_x oder y: Liste mit True oder False der Länge der Punkteliste
        #innere Punkte dürfen immer bewegt werden (vorerst)
        # Liste soll so aussehen: [True, False, False,...]
        #Das würde bedeuten erster punkt ist fixiert, zweiter und dritter nicht...
        

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
if __name__=='__main__':
    s = Shape([(0, 0), (2,8), (10, 10), (10, 0)],[[(1,1), (1,2), (2,1)]])
    display_shape(s)

