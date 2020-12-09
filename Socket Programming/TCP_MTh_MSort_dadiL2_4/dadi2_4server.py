# server
'''
4. The clients send an integer number N and an array of N float values. 
The server will merge sort the numbers received from all clients until it gets an empty array of floats (N=0). 
The server returns to each client the size of the merge-sorted array followed by 
the merge-sorted arrays of all floats from all clients.
'''

import socket
import struct
import pickle
import threading
import os
import time

MSA = []
mylock = threading.Lock()
e = threading.Event()
e.clear()
threads = []
clients = []
done = False

def worker(cs, addr):
    global MSA, mylock, done, e

    while not done:
        N = struct.unpack('!I',cs.recv(4))[0]

        if N == 0 or done is True:
            mylock.acquire()
            done = True
            mylock.release()
            break
        
        cs.send("y".encode('utf8'))
        data = cs.recv(1024)
        a = pickle.loads(data)  # get the floats array from the client 
        
        mylock.acquire()
        MSA.extend(a)
        MSA.sort()
        mylock.release()
        
    if done:
        e.set()


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0",2222))
    s.listen(5)
except socket.error as msg:
        print(msg.strerror)
        exit(-1)

def serverShuttingDown():
    global e, threads, MSA, clients
    e.wait()

    for t in threads:
        t.join()

    for c in clients:
        c.send('n'.encode('utf8'))
        c.sendall(struct.pack('!I',len(MSA)))
        c.sendall(pickle.dumps(MSA))
        c.close()

    os._exit(0)


t = threading.Thread(target=serverShuttingDown, daemon=True)
t.start()

while True:
    cs, addr = s.accept()

    t = threading.Thread(target=worker, args=(cs,addr))
    threads.append(t)
    clients.append(cs)
    t.start()
