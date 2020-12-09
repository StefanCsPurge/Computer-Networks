# server

# The client sends periodical PING datagrams with a random content to a <server> and <port> specified in cmd line. 
# The server returns back (echoes) the same packets (content).
# The client checks the content of the received packets to match what was sent and computes the round trip time
# and displays it to the user for each sent packet.

import socket
import sys

if len(sys.argv) < 2:
    print("You didn't provide a port for your clients!")
    exit(1)

port = int(sys.argv[1])

try:
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("0.0.0.0",port))
except socket.error as e:
    print("Socket error -", e.strerror)
    exit(-1)


while True:
    try: 
        data, addrc = listener.recvfrom(100)
        print("Client {} connected".format(addrc))
    except socket.error as e:
        print("Receive error -", e.strerror)
        exit(-2)

    listener.sendto(data,addrc) # echo the data




