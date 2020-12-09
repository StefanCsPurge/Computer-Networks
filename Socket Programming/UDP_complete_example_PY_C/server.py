
import socket
import sys

if len(sys.argv) < 2:
    print("ERROR, no port provided")
    exit(0)

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
except socket.error:
    print("ERROR, socket opening")
    exit(-1)

s.bind(("0.0.0.0",int(sys.argv[1])))

while(True):
    data, addrc = s.recvfrom(222)
    msg = data.decode('utf8')
    print("Received a datagram: ")
    print(msg)

    try:
        s.sendto("Got your message\n".encode("utf8"),addrc)
    except socket.error:
        print("Error sendto")
        exit(-2)
