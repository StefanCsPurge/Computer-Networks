import socket
import select
import sys
import signal


def signal_handler(sig, frame):
	print("\nYou stopped the chat client, have a nice day! :)")
	exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    if len(sys.argv) < 3:
        print("Usage:\n{} <hostname or IP address> <portno>".format(sys.argv[0]))
        exit(1)

    port = int(sys.argv[2])
    ipaddr = socket.gethostbyname(sys.argv[1])

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Socket creation error -",e.strerror)
        exit(-1)

    try:
        s.connect((str(ipaddr),port))
    except socket.error as e:
        print("Connect error -",e.strerror)
        exit(-1)

    while True:
        try:
            r,w,e = select.select([0,s],[],[])
        except socket.error as e:
            print("Select error -",e.strerror)
            exit(-1)
        
        if 0 in r:
            userInput = input()
            try:
                s.send(userInput.encode('utf8'))
            except socket.error as e:
                print("Send error -",e.strerror)
                exit(-1)
        
        if s in r:
            try:
                data = s.recv(555)
                if data == b'':
                    print("Server closed connection... closing...")
                    exit(2)
            except socket.error as e:
                print("Recv error -",e.strerror)
                exit(2)
            print(data.decode('utf8'))







