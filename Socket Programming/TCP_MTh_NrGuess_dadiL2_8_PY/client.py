'''
A client server implementation in python for the number guess problem. The server chooses a random number. 
The clients connect and send numbers to server. The server returns to each client a status message:
·         ‘H’ – send a larger number
·         ‘S’ – send a lower number
·         ‘G’ – you guessed my number
·         ‘L’ – another client guessed the number. You are a looser !
'''

import random
import socket
import struct
import time

if __name__ == '__main__':
    try:
        s = socket.create_connection(('localhost',1234))
    except socket.error as msg:
        print("Error: ",msg.strerror)
        exit(-1)

    finished = False
    #sr = 1
    #er = 2**17-1
    #random.seed()

    data = s.recv(1024)
    print(data.decode('ascii'))
    step_count = 0

    while not finished:
        #my_num = random.randint(sr,er)
        my_num = int(input("Enter your lucky number: "))
        try:
            s.sendall(struct.pack('!I',my_num))
            answer = s.recv(1)
            numberOfClients = struct.unpack('!I',s.recv(4))[0]
            print(numberOfClients,"clients are competing now")
        except socket.error as msg:
            print('Error: ',msg.strerror)
            s.close()
            exit(-2)
        step_count += 1
        print('Sent ',my_num,' Answer ',answer.decode('ascii'))
        if answer == b'H':
            sr = my_num
        if answer == b'S':
            er = my_num
        if answer == b'G' or answer == b'L':
            finished = True
        time.sleep(0.25)

    s.close()
    if answer == b'G':
        print("I am the winner with",my_num,"in", step_count,"steps")
    else:
        print("I lost !!!")

#    input("Press Enter")
