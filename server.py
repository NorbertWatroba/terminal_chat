import socket
import sys
from _thread import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

ip_address = str(sys.argv[1])
port = int(sys.argv[2])

server.bind((ip_address, port))

server.listen(5)

list_of_clients = []


def client_thread(conn, addr):
    conn.send('Welcome to this chatroom'.center(200, '-'))

    while True:
        try:
            message = conn.recv(2048)
            if message:
                message_to_send = f'<{addr[0]}> {message}'
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(f'{addr[0]} connected')

    start_new_thread(client_thread, (conn, addr))

conn.close()
server.close()
