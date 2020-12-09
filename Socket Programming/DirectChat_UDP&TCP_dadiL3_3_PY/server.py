__author__ = 'spurge'
# server
"""
Implement the Chat server example using UDP and TCP – but this time each client should contact
the server just for registration. All communication happens directly between the peers
(clients) without passing trough the server. Each client maintains an endpoint (TCP/UDP) with the
server just for learning the arrival/departure of other clients.
You create a mesh architecture where all clients connect directly between each others.
"""

import socket
import select
import sys
import signal
import pickle


def signal_handler(sig, frame):
    print("\nYou stopped my chat server :(")
    exit(0)


def getConnectedClients(sockets, crt_sock, rs):
    connected_clients = []
    for clientSock in sockets:
        if clientSock != rs and clientSock != crt_sock:
            connected_clients.append(clientSock.getpeername())
    connected_clients.append(crt_sock.getpeername())
    return connected_clients


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    if len(sys.argv) < 2:
        print("Usage:\n{} <portNo>".format(sys.argv[0]))
        exit(1)

    port = int(sys.argv[1])

    try:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # lose the pesky "address already in use" error message XD
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listener.bind(("0.0.0.0", port))
        listener.listen(10)

    except socket.error as e:
        print("Socket error -", e.strerror)
        exit(-1)

    print("Chat server is up and running")
    read_fds = [listener]
    clients = []
    client_count = 0

    while True:
        try:
            r, w, e = select.select(read_fds, [], [])
        except select.error as e:
            print("Select error -", str(e))
            exit(-1)

        for fd in r:
            if fd == listener:  # handle new client
                try:
                    clSock, addr = listener.accept()
                except socket.error as e:
                    print("Accept error -", e.strerror)
                    exit(-1)

                read_fds.append(clSock)  # add the new client socket to the fds set

                print("+ select_server: new connection from {} on socket {}".format(addr, clSock.getsockname()))
                client_count += 1
                welcomeMsg = "Hi - you are client {} connected to server {}." \
                             "\nThere are {} clients connected.\n" \
                             "Enter CHOOSE to start chatting with a client!"\
                             .format(addr, clSock.getsockname()[0], client_count)
                welcomeMsg_UDPaddr = (welcomeMsg, addr)
                clSock.sendall(pickle.dumps(welcomeMsg_UDPaddr))

            else:  # handle client request
                try:
                    data = fd.recv(256)
                    if data == b'':
                        print("<select_server>: client {} forcibly hung up".format(fd.getpeername()))
                        client_count -= 1
                        fd.close()
                        read_fds.remove(fd)
                        continue
                except socket.error as e:
                    print("Receive error -", e.strerror)
                    exit(-1)

                clientReq = data.decode('utf8')

                if clientReq == "QUIT":
                    msg = "Request granted [{}] - {}. Disconnecting...".format(fd.getpeername(), fd.getsockname())
                    fd.send(msg.encode('utf8'))
                    client_count -= 1
                    fd.close()
                    read_fds.remove(fd)
                elif clientReq == "CHOOSE":
                    fd.sendall(pickle.dumps(getConnectedClients(read_fds, fd, listener)))
