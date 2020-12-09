
import socket
import sys


if len(sys.argv) != 3:
    print("Usage: {} <server_name> <port>\n".format(sys.argv[0]))
    exit(1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ipaddr = socket.gethostbyname(sys.argv[1])
    port = int(sys.argv[2])
except socket.error as e:
    print("Error -",e.strerror)
    exit(2)

message = input("Please enter the message: ")

try:
    s.sendto(message.encode('utf8'),(str(ipaddr),port))
except socket.error:
    print("send error")
    exit(3)

try:
    data, addr = s.recvfrom(256)
except socket.error:
    print("recvfrom error")
    exit(4)

print("Got an ack:",data.decode('utf8'))