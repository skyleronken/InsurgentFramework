from abc import ABCMeta


class Decoder:
    __metaclass__ = ABCMeta
    
    display_name = "Abstract Decoder"
    
    def name(self):
        return self.display_name
    
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