import shape
import tkinter
import random
from algorithms import algorithm

def get_all_pairing_algorithms():
    array = []
    one = None
    array.append(one)
    return array

class PairingAlgorithm(algorithm.Algorithm):

    def pair_shapes(self, shp1, shp2):
        raise NotImplementedError

class AnotherPairingAlgorithm(PairingAlgorithm):

    def pair_shapes(self,shp1, shp2):
        coords_new = []
        if len(shp1.exterior.coords) == len(shp1.exterior.coords):
            coords_num = len(shp1.exterior.coords)
        else:
            print('Fehler')

        shp1_l = shp1.length/coords_num
        shp2_l = shp2.length/coords_num

        shp1_lines = shape.get_lines(shp1)
        shp2_lines = shape.get_lines(shp2)

        shp1_coords_compare = []
        shp2_coords_compare = []

        i = 0
        left = 0

        for _ in range(coords_num):
            distance = shape.get_distance(shp1_lines[i][0],shp1_lines[i][1])
            if distance+left > shp1_l:
                left += distance
                i +=1
                continue
            else:
                distance_on_line = shp1_l-left
                prozent = distance_on_line/distance
                point = shape.point_between_points(shp1_lines[i][0],shp1_lines[i][1],prozent)
                shp1_coords_compare.append(point)
                left = distance-distance_on_line
                if left < shp1_l:
                    i+=1
                elif left > shp1_l:
                    left = -distance_on_line
                elif left == shp1_l:
                    shp1_coords_compare.append(shp1_lines[i][1])
                    left = 0
                    i +=1


    def default_settings(self):
        raise NotImplementedError

    def get_name(self):
        return 'Another Pairing Algorithm'
