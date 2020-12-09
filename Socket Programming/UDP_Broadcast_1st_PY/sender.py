
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except socket.error:
    print("Error on broadcast option")
    exit(-1)

s.sendto("Hello all!".encode(), ("192.168.1.255",5555))

