
from base64 import urlsafe_b64decode, urlsafe_b64encode
from implant.ifcodecs.codec import Codec

class Base64C(Codec):
    
    display_name = "Base 64"
    
    def decode(self, data):
        
        try:
            decoded_data = urlsafe_b64decode(data)
        except Exception, e:
            print e
            raise
        
        return decoded_data
        
    def encode(self, params):
        
        try:
            encoded_data = urlsafe_b64encode(params)
        except Exception, e:
            print e
            raise
        
        return encoded_data