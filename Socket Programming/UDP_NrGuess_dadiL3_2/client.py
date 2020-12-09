"""
A client server implementation in python for the number guess problem. The server chooses a random number.
The clients connect and send numbers to server. The server returns to each client a status message:
·         ‘H’ – send a larger number
·         ‘S’ – send a lower number
·         ‘G’ – you guessed my number
·         ‘L’ – another client guessed the number. You are a looser !
"""

import random
import socket
import struct
import time

if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    finished = False
    sr = 1
    er = 2 ** 17 - 1
    random.seed()
    step_count = 0

    while not finished:
        my_num = random.randint(sr, er)
        try:
            s.sendto(struct.pack('!I', my_num), ("localhost", 1234))
            if step_count == 0:
                print(s.recvfrom(1024)[0].decode('ascii'))  # get welcome message
            answer, addr = s.recvfrom(1)
        except socket.error as msg:
            print('Error2: ', msg.strerror)
            s.close()
            exit(-2)

        step_count += 1
        print('Sent ', my_num, ' Answer ', answer.decode('ascii'))
        if answer == b'H':
            sr = my_num
        if answer == b'S':
            er = my_num
        if answer == b'G' or answer == b'L':
            finished = True
        time.sleep(0.5)

    s.close()
    if answer == b'G':
        print("I am the winner with", my_num, "in", step_count, "steps")
    else:
        print("I lost !!!")
