from abc import ABCMeta, abstractmethod, abstractproperty


class Beacon:
    __metaclass__ = ABCMeta
    
    display_name = "Abstract Beacon"
    
    @abstractproperty
    def name(self):
        return self.display_name
    
    # Trim away all protocol specific artifacts. i.e headers/footers/etc.
    @abstractmethod
    def agnosticize(self, response):
        return response
    
    @abstractmethod
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