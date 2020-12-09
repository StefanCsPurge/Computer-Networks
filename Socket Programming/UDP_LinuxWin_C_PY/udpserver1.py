'''
2. UDP Client in C (on Linux) and Server in Python (on Windows): 
the client sends a message and the Server counts the vowels, 
then sends the number back to the client who displays it.
'''

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0",2222))

buff, addr = s.recvfrom(10)

message = buff.decode('utf-8')

print("From", addr[0], ":", message)

count = 0
for letter in message:
    if letter in "aeiou":
        count += 1

s.sendto(count.to_bytes(4,'little'), addr)
