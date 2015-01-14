import base64

from decoder import Decoder

class Base64(Decoder):
    
    display_name = "Base 64"
    
    def decode(self, params):
        
        data = params['data']
        
        decoded_data = base64.urlsafe_b64decode(data)
        return decoded_data