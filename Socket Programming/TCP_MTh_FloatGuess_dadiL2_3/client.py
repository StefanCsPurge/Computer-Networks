__author__ = 'spurge'
# client
'''
3.   The server chooses a random float number <SRF>. Run multiple clients. 
Each client chooses a random float number <CRF> and send it to the server. 
When the server does not receive any incoming connection for at least 10 seconds 
it chooses the client that has guessed the best approximation (is closest) for 
its own number and sends it back the message “You have the best guess 
with an error of <SRV>-<CRF>”. It also sends to each other client the string 
“You lost !”. 
The server closes all connections after this.
'''

import random
import socket

CRF = round(random.uniform(0.0, 100.0),2)  # get the random float number with 2 digits
print("My number is:",CRF)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",2222))

s.send(str(CRF).encode('utf8'))

data = s.recv(1024)

msg = data.decode()

print(msg)

