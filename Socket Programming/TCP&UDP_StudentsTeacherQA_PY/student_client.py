import socket
import sys
import time
import random
import string
import threading
import signal
import pickle


def signal_handler(sig, frame):
	print("\nYou stopped the student.")
	exit(0)


def leader_worker(leader_sock, group_port):
    while True:
        leader_sock.sendto("leader".encode(), ("<broadcast>",group_port))
        time.sleep(5)


def student_worker(student_sock):
    while True:
        data, addr = student_sock.recvfrom(2048)
        message = data.decode()
        if message != "leader":
            print(f"Got message '{message}' from {addr}")


def getLeaderAddr(student_sock):
    addr_leader = None
    print("Looking for the leader...")
    while addr_leader is None:                                 # get the address of the leader
        data, addr_leader = student_sock.recvfrom(1024)
        if data.decode() != "leader":
            addr_leader = None
        else:
            print("Got the leader:",addr_leader)
            return addr_leader


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage:\n{sys.argv[0]} <group_port> <0 or 1>")
        exit(1)

    group_port = int(sys.argv[1]) 
    is_grLeader = int(sys.argv[2])
    signal.signal(signal.SIGINT, signal_handler)

    try:
        UDP_broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print("Socket error -",e.strerror)
        exit(2)


    if is_grLeader == 1:
        try:
            UDP_broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # TCP socket, comm with teacher
            s.connect(("192.168.72.128",1234))  # connect to the teacher (server)
        except socket.error as e:
            print("Socket error -",e.strerror)
            exit(2)

        t = threading.Thread(target=leader_worker, args=(UDP_broadcast_sock, group_port), daemon = True)
        t.start()
        
        while True:
            data, addrc = UDP_broadcast_sock.recvfrom(256)  # leader got message from student
            s.send(data)
            response = s.recv(2048)
            Q = data.decode()

            completeAnswer = pickle.loads(response)
            QA = f"Q: {Q}? A: {completeAnswer[0]}, {completeAnswer[1]}"
            UDP_broadcast_sock.sendto(QA.encode(), ("<broadcast>",group_port))


    elif is_grLeader == 0:
        UDP_broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # receiver
        UDP_broadcast_sock.bind(('',group_port))

        addr_leader = getLeaderAddr(UDP_broadcast_sock)
        t = threading.Thread(target=student_worker, args=(UDP_broadcast_sock, ), daemon = True)
        t.start()

        while True:  
            randomFloat = random.uniform(0.0, 1.0)
            if randomFloat > 0.5:
                randomString = ''.join(random.choice(string.ascii_letters) for i in range(10))
                UDP_broadcast_sock.sendto(randomString.encode(), addr_leader)
            time.sleep(3)

    else:
        print("Invalid second argument!")

    