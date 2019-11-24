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
