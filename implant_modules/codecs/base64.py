import base64
from codec import Codec

class Base64(Codec):
    
    display_name = "Base 64"
    
    def decode(self, params):
        
        data = params['data']
        
        decoded_data = base64.urlsafe_b64decode(data)
        return decoded_data
        
    def encode(self, params):
        pass