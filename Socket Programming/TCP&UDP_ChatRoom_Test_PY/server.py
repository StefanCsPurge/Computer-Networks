# By spurge

import socket
import pickle
import select

port = 7000

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0",port))
    s.listen(7)
except socket.error as e:
    print("Socket error -", e.strerror)
    exit(-1)



clientsAddr = []
read_fds = [s]

def sendToAll(listener, crt):
    global clientsAddr, read_fds
    print("Connected clients are",clientsAddr)
    for cl in read_fds:
        if cl != listener and cl != crt:
            cl.send(pickle.dumps((crt.getpeername(),clientsAddr)))


while True:
    try:
        r,w,e = select.select(read_fds,[],[])
    except socket.error as e:
        print("Select error -",e.strerror)
        exit(-1)
    
    for fd in r:
        if fd == s:  # handle new connections
            try:
                clSock, addr = s.accept()
            except socket.error as e:
                print("Accept error -",e.strerror)
                exit(-1)

            read_fds.append(clSock)
            clientsAddr.append(clSock.getpeername())
            clSock.send(pickle.dumps((addr,clientsAddr)))
            sendToAll(s,clSock)
    
        else:  # handle data from a client
            try:
                data = fd.recv(1024)
            except socket.error as e:
                print("Recv error -",e.strerror)
                exit(-1)

            if data == b'' or data.decode() == "q":  # client closed connection
                clientsAddr.remove(fd.getpeername())
                sendToAll(s,fd)
                fd.close()
                read_fds.remove(fd)
    

