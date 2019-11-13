from shapely import geometry
import matplotlib.pyplot as plt

class Shape(geometry.Polygon):
    def __init__(self, shell, holes=None, move_restrictions=None, fixed_displacements=None, forces=None):
        super().__init__(shell, holes)

        if move_restrictions is None:
            self.move_restrictions = [False]*len(shell)
        else:
            self.move_restrictions=move_restrictions

        if fixed_displacements is None:
            self.fixed_displacements = [(False),(False)]*len(shell)
        else:
            self.fixed_displacements=fixed_displacements

        if forces is None:
            self.forces = [(False),(False)]*len(shell)
        else:
            self.forces=forces
            
        
##        if fixed_x is None:
##            self.fixed_x = [False]*(len(shell)+1)#möglicher Konflikt, wenn erster Punkt doppelt genannt wird!!!
##        else:
##            self.fixed_x = fixed_x
##
##        if fixed_y is None:
##            self.fixed_y = [False]*(len(shell)+1)
##        else:
##            self.fixed_y = fixed_y


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




















