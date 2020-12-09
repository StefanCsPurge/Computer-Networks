import socket
import select
import sys
import signal


def signal_handler(sig, frame):
	print("\nYou stopped my chat server, have a nice day! :)")
	exit(0)


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    if len(sys.argv) < 2:
        print("Usage:\n{} <portno>".format(sys.argv[0]))
        exit(1)

    port = int(sys.argv[1])

    try:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # lose the pesky "address already in use" error message
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        listener.bind(("0.0.0.0",port))
        listener.listen(10)

    except Exception as e:
        print("Socket option error -",e)
        exit(-1)
    
    print("Room chat server up and running")
    read_fds = [listener]
    client_count = 0

    while True:
        try:
            r,w,e = select.select(read_fds,[],[])
        except socket.error as e:
            print("Select error -",e.strerror)
            exit(-1)
    
        for fd in r:
            if fd == listener:  # handle new connections
                try:
                    clSock, addr = listener.accept()
                except socket.error as e:
                    print("Accept error -",e.strerror)
                    exit(-1)

                read_fds.append(clSock)  # add the client to the fds set

                print("+ selectserver: new connection from {} on socket {}".format(addr, clSock.getsockname()))

                client_count += 1

                welcomeMsg = "Hi - you are client {} connected to server {}.\nThere are {} clients connected. You can start chatting!".format(
                    addr,clSock.getsockname()[0],client_count)

                clSock.send(welcomeMsg.encode('utf8'))

            else:  # handle data from a client
                try:
                    data = fd.recv(256)
                    if data == b'':
                        print("<selectserver>: client {} forcibly hung up".format(fd.getpeername()))
                        client_count -= 1
                        fd.close()
                        read_fds.remove(fd)
                        continue
                except socket.error as e:
                    print("Recv error -",e.strerror)
                    exit(-1)
                # we got some data from the client

                clientMsg = data.decode('utf8')

                if clientMsg == "QUIT":
                    msg = "Request granted [{}] - {}. Disconnecting...".format(fd.getpeername(),fd.getsockname())
                    fd.send(msg.encode('utf8'))

                    allMsg = "<{} - [{}]> disconnected".format(fd.getpeername()[0],fd.getpeername()[1])

                    for client in read_fds:
                        if client != listener and client != fd:
                            client.sendall(allMsg.encode('utf8'))
                    
                    client_count -= 1
                    fd.close()
                    read_fds.remove(fd)
                
                else:
                    allMsg = "<{} - [{}]> {}".format(fd.getpeername()[0],fd.getpeername()[1],clientMsg)

                    for client in read_fds:
                        if client != listener and client != fd:
                            client.sendall(allMsg.encode('utf8'))


'''
GetPeerName() is used to determine who is the client connected to your socket.

GetSockName() is used to determine your own socket properties like which port what IP addresses is the socket bound to.

If your client and server are on the same machine, GetPeerName() and GetSockName() will return the same address but different port numbers.
'''
