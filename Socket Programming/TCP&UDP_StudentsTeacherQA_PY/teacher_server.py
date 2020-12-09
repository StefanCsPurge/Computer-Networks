import socket
import signal
import select
import pickle
import random
import string

def signal_handler(sig, frame):
	print("\nYou stopped the teacher.")
	exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("192.168.72.128",1234))
    listener.listen(10)
    
    read_fds = [listener]
    
    while True:
        r, w, e = select.select(read_fds, [] ,[])

        for fd in r:
            if fd == listener:  # handle new connections
                try:
                    clSock, addr = listener.accept()
                except socket.error as e:
                    print("Accept error -",e.strerror)
                    exit(-1)

                read_fds.append(clSock)  # add the client to the fds set

                print("+ teacher: new connection from {} on socket {}".format(addr, clSock.getsockname()))

            else:   # handle question from a group leader
                try:
                    data = fd.recv(256)
                    if data == b'':
                        print(f"- teacher: group leader {fd.getpeername()} forcibly hung up")
                        fd.close()
                        read_fds.remove(fd)
                        continue
                except socket.error as e:
                    print("Recv error -",e.strerror)
                    exit(-1)

                Q = data.decode()
                print(f"Teacher received question: {Q}")

                A1 = ''.join(random.choice(string.ascii_letters) for i in range(5))
                A2 = [random.choice(range(999)) for i in range(5)]
                completeAnswer = (A1,A2)
                
                fd.sendall(pickle.dumps(completeAnswer))

