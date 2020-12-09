
(Packet Tracer 7.3.1) Network topology in which:

- all local LAN PCs  have intra-lan access to each other
- NAT access is set from all networks to the server in Internet (193.231.20.2) such that its web server is accessible from all LANs
- physical locations for all equipment is set such that

	- 192.168.0.0 is in city Cluj Napoca, building UPC (at least 1km away from FSEGA and UBBMainBuilding)
	- 192.168.1.0 is in city Bucharest, building ROEDU (at least 1km away from other buildings in Bucharest)
	- 192.168.2.0 is in city Cluj Napoca, building FSEGA (at least 1km away from other building in Cluj Napoca)
	- 192.168.3.0 is in city Cluj Napoca, UBBMainBuilding (at least 1km away from other building in Cluj Napoca)
	- 193.231.20.2 is in city Bucharest, building Google (at least 1km away from other buildings in Bucharest)

- the links between R1-R2-R3 are serial links
- routers have DHCP configured where it's needed
- R0 also has NAT configured for accessing the Internet server 193.231.20.2

Requirements:
1.   Be able to access the Internet Server 193.231.20.2 from all networks (NAT)
2.   Be able to access all private LANs from each other – but not from Internet (no router in Internet routes the Private IP address space)
3.   Use RIP to setup routing between (192.168.0.0/24, 192.168.1.0/24, 192.168.2.0/24, 192.168.3.0/24). Do not advertise private networks on the Internet links

![alt text](https://github.com/StefanCsPurge/Computer-Networks/blob/main/PacketTracer%20Project_3%20RIP%2CNAT%2CPhysical%2CCloud/Logical-Topology.png)

![alt text](https://github.com/StefanCsPurge/Computer-Networks/blob/main/PacketTracer%20Project_3%20RIP%2CNAT%2CPhysical%2CCloud/Physical.png)
