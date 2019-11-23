import py_mentat
import py_post
import socket
import pickle
from mentat_connection import Task, Test_connection, HEADERSIZE

#dieses Skript muss aus MarcMentat heraus aufgerufen werden
def main():
    HOST = input('enter host name')
    PORT = input('enter port')
    PORT = int(PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            print('waiting for connection...')
            conn, addr = s.accept()

            with conn:
                print('New Connection\nConnected by', addr)
                
                obj_recv = bytearray()
                data = conn.recv(64)
                obj_length = int(data[:HEADERSIZE].decode('utf-8'))
                obj_recv.extend(data[HEADERSIZE:])
                while len(obj_recv) < obj_length:
                    data = conn.recv(64)
                    obj_recv.extend(data)
                
                task = pickle.loads(obj_recv)
                task.execute(py_mentat, py_post, conn)
                    

            print('Client disconnected')
                    

if __name__=='__main__':
    port = input('enter Mentat port')
    py_mentat.py_connect('',int(port))
    main()
    py_mentat.py_disconnect()
