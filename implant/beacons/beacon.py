from abc import ABCMeta


class Beacon:
    __metaclass__ = ABCMeta
    
    display_name = "Abstract Beacon"
    
    def name(self):
        return self.display_name
    
    # Trim away all protocol specific artifacts. i.e headers/footers/etc.
    def agnosticize(self, response):
        return response
    
    def send_response(self, arguments, results):
        
        while False:
            yield None
    
    def beacon(self, arguments):
        
        #
        # The controller will call this method on all Beacons. The arguments will contain the address/ip/port for the C2 node.
        #
        # The method should return:
        #   - the protocol agnostic undecoded/undecrypted C2 instructions
        #   - Success / Failure
        #
        #
        
        while False:
                yield None