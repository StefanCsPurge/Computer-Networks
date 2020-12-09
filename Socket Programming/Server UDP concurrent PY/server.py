import socket
import struct
from threading import Thread


def f(cSock, cAddr):
    print("Serving client " + str(i))
    val = struct.unpack("!I", cSock.recvfrom(4)[0])[0]
    val = 2 ** val
    print("Sending " + str(val))
    cSock.sendto(struct.pack("!I", val), cAddr)
    cSock.close()


servSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servSock.bind(("0.0.0.0", 2000))
i = 0

while True:
    i += 1
    if i == 1000:
        i = 0
    buff, addr = servSock.recvfrom(4)
    if struct.unpack("!I", buff)[0] != 12:
        continue
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create a new socket for this new client
    clientSock.bind(("0.0.0.0", 2000 + i))  
    servSock.sendto(struct.pack("!I", 2000 + i), addr)  # send the new port nr to the client
    t = Thread(target=f, args=(clientSock, addr,))  # let a thread do the work for this client
    t.start()
