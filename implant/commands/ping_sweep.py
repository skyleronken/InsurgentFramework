from scapy.all import *
import netaddr
from command import Command

NET_ADDR = 'na'

class PingSweep(Command):

    """
    This module will do host discovery using a ping sweep.
    Credit: Matt Wood - @thepacketgeek
    """
    
    display_name = "Ping Sweep"
    index = {NET_ADDR:"Network Range to Scan"}
    
    def execute(self, args):

        success = True
        results = ""

        try:
            # Define IP range to ping
            network = args[NET_ADDR]
     
            # make list of addresses out of network, set live host counter
            addresses = netaddr.IPNetwork(network)
            liveCounter = 0
     
            # Send ICMP ping request, wait for answer
            for host in addresses:
    	        if (host == addresses.network or host == addresses.broadcast):
            		continue
            	resp = sr1(IP(dst=str(host))/ICMP(),timeout=2,verbose=0)
            	if (str(type(resp)) == "<type 'NoneType'>"):
            		results += "%s is down or not responding.\n" % (str(host))
            	elif (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            	    results += "%s is blocking ICMP.\n" % (str(host))
            	else:
            		results += "%s is responding.\n" % (str(host))
            		liveCounter += 1
             
            results += "Out of %s hosts, %s are online." % (str(addresses.size),str(liveCounter))
        except Exception,e :
            results = e
            success = False
            
        return success, results