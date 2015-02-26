from command import Command
import sys
from scapy.all import srp, Ether, ARP, conf

NET_RANGE = 'r'

class ArpScan(Command):
    """
    This module does host discovery via ARP scan
    Credits to: Geo Carp & Jason Ross
    """
    
    display_name = "ARP Scan"
    index = {NET_RANGE:"The network range in CIDR format"}
    
    def execute(self, args):
        
        success = True
        results = ""
        
        net = args.get(NET_RANGE, None)
        
        try:
            conf.verb=0
            alive, dead=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=net),timeout=2)
            for snd,rcv in alive:
                results += rcv.sprintf(r"%Ether.src%,%ARP.psrc%")

        except Exception, e:
            results = e
            success = False
        

        return success, results
        