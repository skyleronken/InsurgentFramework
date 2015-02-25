from json import loads, dumps
from implant.ifcodecs.codec import Codec

class JSONC(Codec):
    
    full_body_encode = True
    display_name = "JSON"
    
    def decode(self, data):
        try:
            decoded_json = loads(data)
            return decoded_json
            
        except Exception, e:
    	    print e
    	
    def encode(self, params):
        try:
            encoded_json = dumps(params)
            return encoded_json
            
        except Exception, e:
            print e