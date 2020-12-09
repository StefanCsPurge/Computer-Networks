#client
'''
 The client sends the complete path to a file. The server returns back the length of the file 
 and its content in the case the file exists. 
 When the file does not exist the server returns a length of -1 and no content. 
 The client will store the content in a file with the same name as the input file 
 with the suffix –copy appended (ex: for f.txt => f.txt-copy).
'''

import socket
import sys
import os
import struct

if len(sys.argv) < 2:
    print("You did not provide a file!")
    exit(1)

fileName = sys.argv[1]

completePath = os.path.abspath(fileName)

print(completePath)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("localhost",2222))

s.sendall(completePath.encode('utf-8'))

fileLen = struct.unpack('!i',s.recv(4))[0]
#data = s.recv(4).decode('utf8')
s.send("y".encode())


if fileLen != -1:
    fileContent = s.recv(fileLen).decode('utf-8')
    fileName = fileName + "-copy"

    f = open(fileName, "w")
    f.write(fileContent)
    f.close()
else:
    print("File does not exist!")




