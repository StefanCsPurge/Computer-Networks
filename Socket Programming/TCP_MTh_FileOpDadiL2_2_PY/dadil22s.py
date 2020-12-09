#server
'''
 The client sends the complete path to a file. The server returns back the length of the file 
 and its content in the case the file exists. 
 When the file does not exist the server returns a length of -1 and no content. 
 The client will store the content in a file with the same name as the input file 
 with the suffix –copy appended (ex: for f.txt => f.txt-copy).
'''

import socket
import os
import threading
import struct

def worker(c, addr):
    clPath = c.recv(1024).decode('utf-8')
    print("From",addr,":",clPath)
    if not os.path.exists(clPath):
        c.sendall(struct.pack('!i',-1))
    else:
        f = open(clPath, "r")
        content = f.read()
        contentLen = len(content)
        c.sendall(struct.pack('!i',contentLen))
        encodedData = content.encode('utf8')
        r = c.recv(1).decode()  # send permission
        if r == 'y':
            c.send(encodedData)
    c.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0",2222))

s.listen(5)

while(True):
    cs, addr = s.accept()

    t = threading.Thread(target=worker, args=(cs,addr))
    t.start()

