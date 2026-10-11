# SERVER

import socket
from _thread import *
import sys

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print('Waiting for eve to connect...')

def threaded_client(conn):
    conn.send(str.encode(''))
    reply = ''
    while True:
        try:
            data = conn.recv(2048).decode()

            if not data:
                print("Disconnected")
                break
            else:
                reply = ""

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

while not connected:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, conn)
    connected = True