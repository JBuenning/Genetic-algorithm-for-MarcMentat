import shape
import tkinter
import random
from algorithms import algorithm

def get_all_pairing_algorithms():
    """Returns an object of every pairing algorithm presen in this file
    
    Returns:
        list: Contains one object of evers pairing algorithm
    """
    lst = []
    return lst

class PairingAlgorithm(algorithm.Algorithm):
    """An algorithm that can merge two shapes into one new shape
    
    Raises:
        NotImplementedError: If the pair_shape function is not overwritten
    """

    def pair_shapes(self, shp1, shp2):
        """Merges two shapes into a new shape
        
        Raises:
            NotImplementedError: If not overwritten
        """
        raise NotImplementedError
