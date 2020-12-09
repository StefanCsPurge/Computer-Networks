# By spurge

import socket
import select
import pickle

port = 7000
clients = []

def updateClients(newClients):
    global clients
    for old in clients:
        if old not in newClients:
            print(f"Client {old[0]}:{old[1]} has disconnected")
    for new in newClients:
        if new not in clients:
            print(f"Client {new[0]}:{new[1]} has connected")
    clients = newClients


try:
    UDPs = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    TCPs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    TCPs.connect(("localhost",port))  # 192.168.72.128 to work in LAN
except socket.error as e:
    print("Socket error -", e.strerror)
    exit(-1)

firstTime = True
myaddr = None


while True:
    try:
        r,w,e = select.select([0, UDPs, TCPs],[],[])
    except socket.error as e:
        print("Select error -",e.strerror)
        exit(-1)

    if TCPs in r:  # get the clients from the server
        try:
            data = TCPs.recv(2048)
            if data == b'':
                print("Server closed connection... closing...")
                exit(2)
        except socket.error as e:
            print("Receive error -", e.strerror)
            exit(3)
        anAddr, newClients = pickle.loads(data)
        updateClients(newClients)
        if firstTime:
            # print("My addr",myaddr)
            myaddr = anAddr
            UDPs.bind(myaddr)
            firstTime = False
    
    if 0 in r:
        msg = input()
        if msg == "QUIT":
            TCPs.send("q".encode())
            TCPs.close()
            UDPs.close()
            break
        for cl in clients:
            if cl != myaddr:
                UDPs.sendto(msg.encode(),cl)
        
    if UDPs in r:
        try:
            data, addr = UDPs.recvfrom(256)
            if data == b'':
                print("Client closed connection...")
                continue
        except socket.error as e:
            print("Receive error -", e.strerror)
            exit(3)
        print(f"{addr} >",data.decode())

    



