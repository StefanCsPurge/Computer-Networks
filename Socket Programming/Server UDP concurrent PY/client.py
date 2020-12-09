import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(struct.pack("!I", 12), ("127.0.0.1", 2000))

port = struct.unpack("!I", sock.recvfrom(4)[0])[0]

print("got port " + str(port))

sock.sendto(struct.pack("!I", 2), ("127.0.0.1", port))

print(struct.unpack("!I", sock.recvfrom(4)[0])[0])

