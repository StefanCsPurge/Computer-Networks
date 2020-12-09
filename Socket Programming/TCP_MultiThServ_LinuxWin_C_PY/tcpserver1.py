'''
1. TCP Client in C (on Linux) and Multi Threaded Server in Python (on Windows): 
the client sends a message and the server displays the ip+port of each client, 
then sends "Message received" back.
'''

import socket
from threading import Thread


def worker(cs, addr):
    ret = "Message received"
    
    while(1):
        message = cs.recv(1024).decode('utf-8')
        print("From", addr, ":",message)
        cs.send(ret.encode('utf-8'))
        if "close" in message:
            break

    print("Connection to",addr,"was closed")
    cs.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0",2222))

s.listen(5)

while(1):
    cs,addr = s.accept()
    thr = Thread(target = worker, args = (cs,addr))
    thr.start()
