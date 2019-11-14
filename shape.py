from shapely import geometry
import matplotlib.pyplot as plt
import numpy as np

def evened_out_point(point, neighbour1, neighbour2, restriction=False):
    px, py = point
    n1x, n1y = neighbour1
    n2x, n2y = neighbour2
    mx = (n2x + n1x)/2
    my = (n2y + n1y)/2
    
    if restriction:
        restriction_x, restriction_y = restriction
        #in Matrixschreibweise AX=B
        try:
            A = np.array([[restriction_x, n1y-n2y],[restriction_y, n2x-n1x]])
            B = np.array([mx-px, my-py])
            t,u = np.linalg.solve(A,B)

            x = px + t*(restriction_x)
            y = py + t*(restriction_y)
        except:
            #wenn der Punkt sich wegen der restriction nur senkrecht zu den Nachbarpunkten bewegen dürfte
            x, y = point

    else:
        #in Matrixschreibweise AX=B
        A = np.array([[n2x-n1x, n1y-n2y],[n2y-n1y, n2x-n1x]])
        B = np.array([mx-px, my-py])
        t,u = np.linalg.solve(A,B)

        x = px + t*(n2x - n1x)
        y = py + t*(n2y - n1y)
    return(x,y)

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


if __name__=='__main__':
    print(evened_out_point((1,4), (0,0), (10,0), restriction=(0,1)))
















