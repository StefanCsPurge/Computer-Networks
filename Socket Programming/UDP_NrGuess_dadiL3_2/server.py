"""
Implement the Python concurrent example from lab2 to work with UDP.
You no longer need threads to be able to serve multiple clients – so the implementation should be much shorter.
"""
import socket
import random
import struct

random.seed()
start = 1
stop = 2 ** 17 - 1
my_num = random.randint(start, stop)
print('Server number: ', my_num)

clients = {}
client_count = 0


def resetSrv():
    global my_num, clients, client_count, rs
    print("all clients are finished now - server is resetting...")
    while client_count > 1:
        rs.recvfrom(4)
        client_count -= 1
    client_count = 0
    clients = {}
    my_num = random.randint(start, stop)
    print('\nServer number: ', my_num)


def analyzeNumber(addrc):
    global clients, my_num, rs
    cnr = clients[addrc]
    if cnr > my_num:
        rs.sendto(b'S', addrc)
    elif cnr < my_num:
        rs.sendto(b'H', addrc)
    elif cnr == my_num:
        rs.sendto(b'G', addrc)
        print('We have a winner:', addrc)
        for c in clients:
            if c != addrc:
                rs.sendto(b'L', c)
                print("Client ", c, " looser")
        resetSrv()


if __name__ == '__main__':
    rs = "rendezvous socket"
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rs.bind(('0.0.0.0', 1234))
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    while True:
        encoded_data, addr = rs.recvfrom(4)
        cNumber = struct.unpack('!I', encoded_data)[0]

        if addr not in clients:     # we deal with the new client
            print('client #', client_count, 'from: ', addr)
            message = 'Hello client #' + str(client_count) + ' ! You are entering the number guess competition now !'
            rs.sendto(bytes(message, 'ascii'), addr)
            client_count += 1

        clients[addr] = cNumber
        analyzeNumber(addr)
