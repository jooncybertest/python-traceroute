'''
Created on Mar 1, 2020

@author: techstaff
'''
import sys
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute


if (len(sys.argv) != 2):
    hostname = "mn.gov"
else:
    hostname = sys.argv[1]

ip = socket.gethostbyname(hostname)

print("The IP address for " + hostname + " is " + str(ip))

res, _ = traceroute(ip,maxttl=64,verbose = 0)

res.show()