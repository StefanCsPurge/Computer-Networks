# server
"""
The client sends a domain name taken from the command line (Ex: www.google.com) to the server. 
The server opens a TCP connection to the IP address corresponding to the received domain name on port 80 (called HTTP-Srv). 
It sends on the TCP connection the string: “GET / HTTP/1.0\n\n” and relays the answer back to the client. 
When HTTP-Srv closes connection to the server, the server closes the connection to the client at its turn. 
"""

import socket
import threading

def worker(cs, addr):
    data = cs.recv(555)

    domain = data.decode('utf8')
    IP = socket.gethostbyname(domain)
    print("The IP of",domain,"is",IP)

    try:
        HTTP_Serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HTTP_Serv.connect((domain,80))
        request = "GET / HTTP/1.0\n\n"
        HTTP_Serv.send(request.encode('utf8'))
    except socket.error as e:
        print("Socket error -",e.strerror)
        exit(-1)

    HTTPdata = HTTP_Serv.recv(1024)
    #print("Response is:",HTTPdata.decode('utf8'))
    cs.sendall(HTTPdata)

    HTTP_Serv.close()
    cs.close()



try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0",2222))
    s.listen(5)
except socket.error as msg:
        print(msg.strerror)
        exit(-1)


while True:
    cs, addrc = s.accept()

    t = threading.Thread(target=worker, args=(cs,addrc))
    t.start()