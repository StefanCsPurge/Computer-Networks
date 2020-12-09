__author__ = 'spurge'
# server
'''
3.   The server chooses a random float number <SRF>. Run multiple clients. 
Each client chooses a random float number <CRF> and send it to the server. 
When the server does not receive any incoming connection for at least 10 seconds 
it chooses the client that has guessed the best approximation (is closest) for 
its own number and sends it back the message “You have the best guess 
with an error of <SRV>-<CRF>”. It also sends to each other client the string 
“You lost !”. 
The server closes all connections after this.
'''
import socket
import threading
import random
import sys

SRF = round(random.uniform(0.0, 100.0),2)
print('Server number:',SRF)

threads = []
minDiff = 300000.0
time_ended = False
mylock = threading.Lock()

def worker(cs,addrc):
    global time_ended, mylock, minDiff, SRF

    data = cs.recv(8)
    CRF = float(data.decode('utf8'))
    diff = abs(SRF - CRF)
    print("Client",addrc,"is as close as",round(diff,2))

    mylock.acquire()
    minDiff = min(diff, minDiff)
    mylock.release()

    while not time_ended: 
        continue

    if diff == minDiff:
        msg = "You have the best guess with an error of " + str(round(diff,2))
        cs.send(msg.encode('utf8'))
    else:
        cs.send("You lost !".encode('utf8'))
    cs.close()


if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0',2222))
        s.listen(7)
        s.settimeout(10)
    except socket.error as e:
        print(e.strerror)
        exit(-1)

    while True:
        try:
            cs, addrc = s.accept()
        except socket.timeout:
            print("10 seconds passed, calculating the results and shutting down...")
            time_ended = True
            for t in threads:
                t.join()
            print("all threads are finished now")
            break
        t = threading.Thread(target=worker, args=(cs,addrc))
        threads.append(t)
        t.start()
        
        
