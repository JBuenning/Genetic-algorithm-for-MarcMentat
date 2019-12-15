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
    lst = [BasicPairing(),BooleanPairing()]
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

class BasicPairing(PairingAlgorithm):
    def pair_shapes(self,shape1,shape2):
        random_range = 0.2

        coords1 = shape1.exterior.coords[:-1]
        coords2 = shape2.exterior.coords[:-1]
        coords = [coords1,coords2]
        if len(coords1) != len(coords2):
            print('Achtung ganz böse Ausnahme hier fehlt noch etwas Programmierarbeit um beide Listen auf die gleich eLänge zu bringen')
        
        if False:
            start_points = []
            smallest_distance = 9999999
            for point1 in coords1:
                for point2 in coords2:
                    if shape.distance(point1,point2) < smallest_distance:
                        smallest_distance = shape.distance(point1,point2)
                        start_points = [point1,point2]
            coords_sorted = []
            for i in range(2):
                array = []
                j = coords[i].index(start_points[i])
                while j < len(coords[i]):
                    array.append(coords[i][j])
                    j += 1
                for point in coords[i]:
                    if point == start_points[i]:
                        break
                    else:
                        array.append(point)
                coords_sorted.append(array)
            coords1,coords2 = coords_sorted

        coords_new = []
        for i in range(len(coords1)):
            coords_new.append(shape.point_between_points(coords1[i],coords2[i],0.5))
        ### Hier muss noch überprüft werden ob denn restrictions usw bei beidne shapes übereinstimmen
        s = shape.Shape(coords_new, shape1.interiors, shape1.move_restrictions, shape1.fixed_displacements, shape1.forces)
        if not s.is_valid or not s.is_simple:
            s = random.choice([shape1,shape2]) # different solution in the future
        return s

    def default_settings(self):
        pass

    def get_name(self):
        return 'Basic Pairing'

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