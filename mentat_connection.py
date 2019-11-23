import random
import pickle

HEADERSIZE = 20

#die Instanzen der hier definierten Klassen werden vom Hauptprogramm zu Mentat geschickt
#dort wird das Objekt entpackt und die methode execute aufgerufen
class Task:
    def __init__(self, coords, forces, fixed_displacements):
        self.coords = coords
        self.forces = forces
        self.fixed_displacements = fixed_displacements

    def execute(self, py_mentat, py_post, socket_connection):
        py_mentat.py_send('*clear_geometry')
        py_mentat.py_send('*clear_mesh')
        for point in self.coords:
            py_mentat.py_send("*add_points {},{},0".format(point[0], point[1]))

        py_mentat.py_send('*set_curve_type line')

        for i in range(1, len(self.coords)):
            py_mentat.py_send('*add_curves {},{}'.format(i, i+1))
        py_mentat.py_send('*add_curves {},1'.format(len(self.coords)))

        obj_bytes = pickle.dumps('evaluation')# hier wird später der ermittelte Wert zurückgesendet
        if len(str(len(obj_bytes)))>HEADERSIZE:
            raise Exception('Length of the object to send exceeds header size')
        
        header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
        socket_connection.sendall(header + obj_bytes)

class Test_connection:
    def __init__(self, testobject):
        self.testobject = testobject
        
    def execute(self, py_mentat, py_post, socket_connection):
        obj_bytes = pickle.dumps(self.testobject)

        if len(str(len(obj_bytes)))>HEADERSIZE:
            raise Exception('Length of the object to send exceeds header size')
        
        header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
        socket_connection.sendall(header + obj_bytes)
