import socket
import select
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print('Correct usage: script, ip address, port number')
    exit()
ip_address = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((ip_address, port))

while True:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socket in sockets_list:
        if socket == server:
            message = socket.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.write('<You>')
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()
