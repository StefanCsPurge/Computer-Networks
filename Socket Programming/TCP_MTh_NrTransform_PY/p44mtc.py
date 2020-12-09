 
# client
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
s.connect(("localhost",8888))

n = int(input("Insert your number (max 4 digits): "))

s.send(str(n).encode())

noInWords = s.recv(99)

print(noInWords.decode())
