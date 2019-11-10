from shapely import geometry

class Shape(geometry.Polygon):
    def __init__(self, shell, holes=None, fixed_x=None, fixed_y=None):
        super().__init__(shell, holes)
        self.fixed_x = fixed_x
        self.fixed_y = fixed_y

    #Methoden und Attribute, die schon da sind:
        
    #object.exterior.coords -> Liste mit äußeren Koordinaten [(x,y),(x,y)...]
    #object.interior.coords -> innere Koordinaten[[(x,y),(x,y)...],[...],...]
    #object.is_valid -> True wenn valid
    #object.is_simple -> True wenn keine Überschneidung mit sich selbst
    #object.area
    #...
    
