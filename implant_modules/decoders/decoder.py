from abc import ABCMeta, abstractmethod, abstractproperty


class Decoder:
    __metaclass__ = ABCMeta
    
    display_name = "Abstract Decoder"
    
    @abstractproperty
    def name(self):
        return self.display_name
    
    @abstractmethod
    def decode(self, arguments):
        
        #
        # The controller will call this method on all Decoders. The arguments will contain any relevant keys, etc.
        #
        # The method should return:
        #   - the decoded data
        #   - Any relevant Success / Failure
        #
        #
        
        while False:
                yield None