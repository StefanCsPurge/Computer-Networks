(Packet Tracer 6.2) 
I created a Mini-Internet consisting of: DHCP, DNS and Web servers, endpoint devices, switches, routers.

The entire network has:

	IP: 59.116.215.0
	Mask: 255.255.255.0 (/24)

	Subnetworks that must have:
	N1: 40 IP's (59.116.215.64/26, 255.255.255.192)
	N2: 24 IP's (59.116.215.0/27, 255.255.255.224)
	N3: 20 IP's (59.116.215.32/27, 255.255.255.224)
	N4: 12 IP's (59.116.215.128/28, 255.255.255.240)
	N5:  4 IP's (59.116.215.144/29, 255.255.255.248)

The adresses were found by splitting the initial network recursively (binary tree like).

Each server in each LAN also has the DHCP service enabled. 
The Router4 was manually set to also work as a DHCP server, because its LAN does not have a server. 

![alt text](https://github.com/StefanCsPurge/Computer-Networks/blob/main/PacketTracer%20Mini-Internet%201/Mini-Internet-1.png)


