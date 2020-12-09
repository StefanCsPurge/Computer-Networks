__author__ = 'spurge'
# client
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
    print("\nHave a nice day! :)")
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    if len(sys.argv) < 3:
        print("Usage:\n{} <hostname or IP address> <portNo>".format(sys.argv[0]))
        exit(1)

    port = int(sys.argv[2])
    ipaddr = socket.gethostbyname(sys.argv[1])

    try:
        TCP_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_sock.connect((str(ipaddr), port))

        UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print("Socket error -", e.strerror)
        exit(-1)

    firstTime = True
    clientChosen = False
    currentClient = None
    connectedClients = []

    while True:
        try:
            r,w,e = select.select([0, TCP_sock, UDP_sock], [], [])
        except socket.error as e:
            print("Select error -", e.strerror)
            exit(-1)

        if 0 in r:
            clientMsg = input()
            try: 
                if clientMsg in ("QUIT", "CHOOSE"):
                    clientChosen = False
                    TCP_sock.send(clientMsg.encode('utf8'))
                elif clientMsg.isdigit() and not clientChosen:
                    cl = int(clientMsg)
                    if cl < 1 or cl > len(connectedClients):
                        print("Index out of bounds!")
                    else:
                        currentClient = connectedClients[cl-1]
                        print("Opened chat with",currentClient)
                        clientChosen = True
                        
                elif clientChosen:  # send a message to the chosen client using UDP
                    UDP_sock.sendto(clientMsg.encode('utf8'),currentClient)
                else:
                    print("Invalid command! Please use CHOOSE or QUIT")

            except socket.error as e:
                print("Send error -", e.strerror)
                exit(-2)

        if UDP_sock in r:  # get the message from other client
            try:
                data, addr = UDP_sock.recvfrom(256)
                if data == b'':
                    print("Client closed connection...")
                    continue
            except socket.error as e:
                print("Receive error -", e.strerror)
                exit(3)
            print(f"{addr} >",data.decode('utf8'))

        if TCP_sock in r:
            try:
                data = TCP_sock.recv(2048)
                if data == b'':
                    print("Server closed connection... closing...")
                    exit(2)
            except socket.error as e:
                print("Receive error -", e.strerror)
                exit(3)
            
            if firstTime:
                neededWelcome = pickle.loads(data)
                print(neededWelcome[0])
                UDP_sock.bind(neededWelcome[1])
                firstTime = False
            else:
                try:
                    connectedClients = pickle.loads(data)
                    print("Choose client to chat with:")
                    for i in range(len(connectedClients)-1):
                        print(f"-> {i+1} ", connectedClients[i])
                except:
                    incomingMsg = data.decode('utf8')
                    print(incomingMsg)



