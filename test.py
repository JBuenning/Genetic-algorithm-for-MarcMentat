import py_mentat
import py_post

def read_in(shape_coords, shape_fixed_dispacements, shape_forces):
        print('reading in shape')
        py_mentat.py_send('*new_model yes')

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

def post_processing():
    py_mentat.py_send('*post_open_default')
    py_mentat.py_send('*post_value Equivalent Von Mises Stress')
    py_mentat.py_send('*post_contour_bands')
    n_id = py_mentat.py_get_int("scalar_max_node()")
    value = py_mentat.py_get_float('scalar_1({})'.format(n_id))
    if value:
        print('the result is ', value)
    else:
        print('no value')

def main():
    shell = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),
             (14,1),(14,2),(14,3),
             (13,3),(12,3),(11,3),(10,3),(9,3),(8,3),(7,3),(6,3),(5,3),(4,3),(3,3),
             (3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(3,12),(3,13),
             (3,14),(2,14),(1,14),
             (0,14),(0,13),(0,12),(0,11),(0,10),(0,9),(0,8),(0,7),(0,6),(0,5),(0,4),(0,3),(0,2),(0,1)]

    fixed_displacements = [(False,False)]*39 + [(True,True)]*4 + [(False,False)]*13

    forces = [(False,False)]*17 + [(0, -100)] + [(False,False)]*38

    read_in(shell, fixed_displacements, forces)
    post_processing()

if __name__=='__main__':
    py_mentat.py_connect("",40007)
    main()
    py_mentat.py_disconnect()