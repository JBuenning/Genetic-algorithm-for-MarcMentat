import random
import pickle

HEADERSIZE = 20

#die Instanzen der hier definierten Klassen werden vom Hauptprogramm zu Mentat geschickt
#dort wird das Objekt entpackt und die methode execute aufgerufen
class Task:
    def execute(self, py_mentat, py_post, socket_connection):
        py_mentat.py_send("*add_nodes {},{},0".format(random.randint(0,200), random.randint(0,200)))

class Test_connection:
    def __init__(self, testobject):
        self.testobject = testobject
        
    def execute(self, py_mentat, py_post, socket_connection):
        obj_bytes = pickle.dumps(self.testobject)

        if len(str(len(obj_bytes)))>HEADERSIZE:
            raise Exception('Length of the object to send exceeds header size')
        
        header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
        socket_connection.sendall(header + obj_bytes)
