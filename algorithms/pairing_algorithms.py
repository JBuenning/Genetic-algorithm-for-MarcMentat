import shape
import tkinter
import random
from algorithms import algorithm

def get_all_pairing_algorithms():
    array = []
    one = AdvancedPairing()
    array.append(one)
    return array

class PairingAlgorithm(algorithm.Algorithm):

    def pair_shapes(self, shp1, shp2):
        raise NotImplementedError

class AdvancedPairing(PairingAlgorithm):
    def pair_shapes(self, shp1, shp2):
        intersection = shp1.intersections(shp2)
        for shp in  [shp1,shp2]:
            diff = list(shp.difference(intersections))
            inner_points=  []
            for point in diff:
                if point in intersection:
                    inner_points.append(point)

    def default_settings(self):
        pass
    
    def get_name(self):
        raise 'Advanced Pairing'
