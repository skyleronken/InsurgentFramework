from json import loads
from codec import Codec

class JSONC(Codec):
    
    display_name = "JSON"
    
    def decode(self, data):
        try:
            decoded_json = loads(data)
            return decoded_json
            
        except Exception, e:
    	    print e
    	
    def encode(self, params):
        pass