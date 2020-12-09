# client
"""
The client sends a domain name taken from the command line (Ex: www.google.com) to the server. 
The server opens a TCP connection to the IP address corresponding to the received domain name on port 80 (called HTTP-Srv). 
It sends on the TCP connection the string: “GET / HTTP/1.0\n\n” and relays the answer back to the client. 
When HTTP-Srv closes connection to the server, the server closes the connection to the client at its turn. 
"""
import socket
import sys

if len(sys.argv) < 2:
    print("You didn't provide a domain name!")
    exit(-1)

domain = sys.argv[1]

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print("Socket error -",e.strerror)
    exit(-1)

s.connect(("localhost",2222))

s.sendall(domain.encode('utf8'))

data = s.recv(2048)

response = data.decode('utf8')

print("The HTTP answer is:\n")
print(response)
