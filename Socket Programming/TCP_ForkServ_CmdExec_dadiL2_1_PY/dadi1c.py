# The client takes a string from the command line and sends it to the server. 
# The server interprets the string as a command with its parameters. 
# It executes the command and returns the standard output and the exit code to the client.

import sys
import socket
import pickle
import struct

myCmdStr = str (' '.join(sys.argv[1:]))
# print(myCmdStr)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1",2222))

    s.send(myCmdStr.encode())

    data = s.recv(2048)

except socket.error as e:
    print("Socket error -",e.strerror)
    exit(-1)

s.send(b'y')  # receive confirmation

output = data.decode()

print("The output is:\n{}".format(output))

retCode = struct.unpack('!i',s.recv(4))[0]
s.close()

print("The exit code is:", retCode)



