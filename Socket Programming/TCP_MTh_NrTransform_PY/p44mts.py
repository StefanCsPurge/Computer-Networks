# Serv transforma o cifra in cuvinte [1234-Una mii doua sute trei zeci si patru] (max 4 cifre)
# TCP multi-threaded server
#!/usr/bin/env python
import signal
import sys
import threading 
import socket


# here is the implementation of the number transforming

units = ["zero", "unu", "doi", "trei", "patru", "cinci", "sase", "sapte", "opt", "noua"]
zeci = ["zero", "zece", "douazeci", "treizeci", "patruzeci", "cincizeci", "saizeci", "saptezeci", "optzeci", "nouazeci"]
specialZeci = {"si unu": "unsprezece",
               "si doi": "doisprezece",
               "si trei": "treisprezece",
               "si patru": "paisprezece",
               "si cinci": "cincispreceze",
               "si sase": "saisprezece",
               "si sapte": "saptesprezece",
               "si opt": "optsprezece",
               "si noua": "nouasprezece"}

sute = ["zero", "o suta", "doua sute", "trei sute", "patru sute", "cinci sute", "sase sute", "sapte sute", "opt sute",
        "noua sute"]
mii = ["zero", "o mie", "doua mii", "trei mii", "patru mii", "cinci mii", "sase mii", "sapte mii", "opt mii",
       "noua mii"]



def worker(cs):
	number = int(cs.recv(4))  # get the number sent by the client	
	if number not in range(10000):
	    print("Boss eu ti-am zis sa respecti regulile , oof")
	    exit()

	components = [units[number % 10]]
	number //= 10

	if number:
	    if components[-1] == "zero":
                components.pop()
	    else:
                components.append("si")
	    if len(components) and number % 10 == 1:
                key = "si " + components[0]
                components.clear()
                components.append(specialZeci[key])
	    else:
                components.append(zeci[number % 10])

	    number //= 10

	    if number:
                if components[-1] == "zero":
                    components.pop()
                components.append(sute[number % 10])

                number //= 10

                if number:
                    if components[-1] == "zero":
                        components.pop()
                    components.append(mii[number % 10])

	components.reverse()

	cs.send(' '.join(components).encode()) # send the result
	cs.close()


def signal_handler(sig, frame):
	print("\nYou stopped my number converting server, have a nice day! :)")
	exit()


if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
	s.bind(("0.0.0.0",8888))
	s.listen(7)  
	print("Server started...")
	signal.signal(signal.SIGINT, signal_handler)	

	while(True):
		cs, addr = s.accept()
		t = threading.Thread(target=worker, args=(cs,))
		t.start()



