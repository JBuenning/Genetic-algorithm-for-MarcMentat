import tkinter as tk
import time

def get_all_algorithms():#to be improved
    '''returns dictionary with all algorithms'''
    algo_list = [Basic_read_in()]
    algo_dict = {}
    for algo in algo_list:
        algo_dict[algo.get_name()] = algo
    
    return algo_dict


class Read_in_algorithm:

    def execute(self, shape_coords, shape_fixed_dispacements, shape_forces, py_mentat):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_settings_frame(self, master):
        frame = tk.Frame()
        label = tk.Label(frame, text='no settings available')
        label.pack()
        return frame

class Basic_read_in(Read_in_algorithm):

    def get_name(self):
        return 'basic read in algorithm'

    def execute(self, shape_coords, shape_fixed_dispacements, shape_forces, py_mentat):
        print('reading in shape')
        py_mentat.py_send('*post_close')
        py_mentat.py_send('*clear_mesh')
        py_mentat.py_send('*clear_geometry')
        py_mentat.py_send('*remove_all_applys')
        py_mentat.py_send('*new_geometry *geometry_type mech_three_beam_ela')
        py_mentat.py_send('*new_mater standard *mater_option general:state:solid *mater_option general:skip_structural:off')
        py_mentat.py_send('*remove_unused_geoms')
        py_mentat.py_send('*remove_unused_maters')

        #points
        for point in shape_coords:
            py_mentat.py_send("*add_points {},{},0".format(point[0], point[1]))

        #curves
        py_mentat.py_send('*set_curve_type line')
        for i in range(1, len(shape_coords)):
            py_mentat.py_send('*add_curves {},{}'.format(i, i+1))
        py_mentat.py_send('*add_curves {},1'.format(len(shape_coords)))

        #automesh
        py_mentat.py_send('*af_planar_trimesh all_existing')

        #geometric properties
        py_mentat.py_send('*new_geometry *geometry_type mech_planar_pstress')
        py_mentat.py_send('*geometry_param norm_to_plane_thick 10')
        py_mentat.py_send('*add_geometry_elements all_existing')

        #material properties
        py_mentat.py_send('*new_mater standard *mater_option general:state:solid *mater_option general:skip_structural:off')
        py_mentat.py_send('*mater_param structural:youngs_modulus 10000')
        py_mentat.py_send('*mater_param structural:poissons_ratio 0.3')
        py_mentat.py_send('*add_mater_elements all_existing')

        #fixed displacements
        for i, fdp in enumerate(shape_fixed_dispacements):
            if [value for value in fdp if value]:
                py_mentat.py_send('*new_apply *apply_type fixed_displacement')
                if fdp[0]:
                    py_mentat.py_send('*apply_dof x *apply_dof_value x')
                if fdp[1]:
                    py_mentat.py_send('*apply_dof y *apply_dof_value y')
                py_mentat.py_send('*add_apply_points {} #'.format(i+1))

        #forces
        for i, force in enumerate(shape_forces):
            if [value for value in force if value]:
                py_mentat.py_send('*new_apply *apply_type point_load')
                if force[0]:
                    py_mentat.py_send('*apply_dof x *apply_dof_value x {}'.format(force[0]))
                if force[1]:
                    py_mentat.py_send('*apply_dof y *apply_dof_value y {}'.format(force[1]))
                py_mentat.py_send('*add_apply_points {} #'.format(i+1))

        #job
        py_mentat.py_send('*prog_use_current_job on *new_job structural')
        py_mentat.py_send('*add_post_var von_mises')
        py_mentat.py_send('*submit_job 1')

        #time.sleep(1)#for simulating complicated task
