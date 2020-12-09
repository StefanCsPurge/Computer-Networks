import socket
import os
import subprocess
import struct

def child(cs):
    #print('\nA new child ',  os.getpid())
    cmdStr = cs.recv(111).decode()   
    cmdStrA = cmdStr.split()
    try:
        result = subprocess.run(cmdStrA, stdout=subprocess.PIPE)
    except Exception as e:
        print("Command execution error -",str(e))
        cs.send(str(e).encode('utf8'))
        os._exit(1)
    
    cs.sendall(result.stdout)
    os._exit(0)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(("0.0.0.0",2222))
    s.listen(7)

    while(True):
        cs, addr = s.accept()
        newpid = os.fork()
        if newpid == 0:
            child(cs)
        else:
            pids = (os.getpid(), newpid)
            print("parent: %d, child: %d" % pids)
            pid, status = os.wait()
            #print(status,(status>>8))
            returnCode = status>>8

            ack = cs.recv(1)
            if ack == b'y':
                cs.send(struct.pack('!i',returnCode))
            cs.close()


