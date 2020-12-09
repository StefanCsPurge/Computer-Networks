# client
"""
4. The clients send an integer number N and an array of N float values. 
The server will merge sort the numbers received from all clients until it gets an empty array of floats (N=0). 
The server returns to each client the size of the merge-sorted array followed by 
the merge-sorted arrays of all floats from all clients.
"""

import socket
import pickle
import struct
import random

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print("Error at socket creation - ",e.strerror)
    exit(-1)

s.connect(("localhost",2222))

while True:

    N = int(input("Enter N: "))
    s.sendall(struct.pack('!I',N))
    response = s.recv(1).decode('utf8')

    if response == 'n':
        MSN = struct.unpack('!I',s.recv(4))[0]
        #s.send('y'.encode('utf8'))
        data = s.recv(1024)
        MSA = pickle.loads(data)
        print("Merge sorted array: ", MSA)
        break
    
    print("Generating {} float values...".format(N))
    a = []
    for i in range(N):
        a.append(round(random.uniform(0,100),2))
    print(a)
    data = pickle.dumps(a)
    s.sendall(data)

