import shape
import tkinter as tk
from tkinter import ttk
import random
from algorithms import algorithm

def get_all_pairing_algorithms():
    """Returns an object of every pairing algorithm presen in this file
    
    Returns:
        list: Contains one object of evers pairing algorithm
    """
    lst = [BooleanPairing()]
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
    
    def pair_forces(self, force1, force2):
        return force1

    def pair_move_restrictions(self, move_restriction1, move_restriction2):
        return move_restriction1
    
    def pair_fixed_displacements(self, fixed_displacement1, fixed_displacement2):
        return fixed_displacement1

class BooleanPairing(PairingAlgorithm):

    def pair_shapes(self, shp1, shp2, *args):
        boolean_fncs = [shp1.union,shp1.intersection]
        if args:
            if args[0]:
                polygon_new = boolean_fncs[0](shp2)
            else:
                polygon_new = boolean_fncs[1](shp2)
        else:
            polygon_new = random.choice(boolean_fncs)(shp2)

        coords_polygon_new = polygon_new.exterior.coords[:-1]
        coords_new = []
        move_restrictions_new = []
        fixed_displacements_new = []
        forces_new = []
        i = 0
        for coord in coords_polygon_new:
            if coord in shp1.exterior.coords or coord in shp2.exterior.coords:
                coords_new.append(coord)
                if coord in shp1.exterior.coords:
                    shp = shp1
                elif coord in shp2.exterior.coords:
                    shp = shp2
                coords = shp.exterior.coords[:-1]
                index = coords.index(coord)
                move_restrictions_new.append(shp.move_restrictions[index])
                forces_new.append(shp.forces[index])
                fixed_displacements_new.append(shp.fixed_displacements[index])
                i += 1
            else:
                if self.change_coords_num_allowed:
                    coords_new.append(coord)
                    # calculate new move restrictions,forces and fixed displacemnts

        return shape.Shape(coords_new,
                            move_restrictions=move_restrictions_new,
                            fixed_displacements=fixed_displacements_new,
                            forces=forces_new)

    def default_settings(self):
        self.change_coords_num_allowed = False

    def get_settings_frame(self,master):

        def cb_fnc():
            # self.change_coords_num_allowed = self.cb_status.get()
            print('not supported yet')
            self.cb_status.set(False)

        frame = tk.Frame(master)
        tk.Label(frame, text='change of the number of coords is allowed').pack(side='left')
        self.cb_status = tk.BooleanVar()
        self.cb_status.set(False)
        ttk.Checkbutton(frame,command= cb_fnc, variable = self.cb_status).pack(side='right')
        return frame

    def get_name(self):
        return 'Boolean Pairing'

    def get_description(self):
        return '''Intersection or Union of both shapes. Intersection should be used when the area needs to be decreased and union should be used when the area needs to be increased.
        If the number of points has to stay the same newly created points during the intersection will be removed'''