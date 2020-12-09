import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(('',5555)) 

    data, addr = s.recvfrom(222)
    
except socket.error as e:
    print("Error -",e.strerror)
    exit(-1)

msg = data.decode()

print(msg)
