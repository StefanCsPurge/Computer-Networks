# client

# The client sends periodical PING datagrams with a random content to a <server> and <port> specified in cmd line. 
# The server returns back (echoes) the same packets (content).
# The client checks the content of the received packets to match what was sent and computes the round trip time
# and displays it to the user for each sent packet.

import socket
import string
import random
import sys
import time

if len(sys.argv) < 3:
    print("Usage:\n{} <server> <port>".format(sys.argv[0]))
    exit(1)

servaddr = socket.gethostbyname(sys.argv[1])
port = int(sys.argv[2])

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print("Socket error -", e.strerror)
    exit(-1)

while True:
    randomString = ''.join(random.choice(string.ascii_letters) for i in range(99))
    
    print("Sending PING datagram to ({},{}) - ".format(servaddr,port),end='')
    start_time = time.time()
    try:
        s.sendto(randomString.encode('utf8'),(str(servaddr),port))
        data, addr = s.recvfrom(100)
    except socket.error as e:
        print("Error -",e.strerror)
        exit(-2)
    
    if data.decode('utf8') != randomString:
        print("data was corrupted! - ",end='')
    else:
        print("correct data received - ",end='')

    print("%s s round trip time" % (time.time() - start_time))
    
    time.sleep(1.5)




