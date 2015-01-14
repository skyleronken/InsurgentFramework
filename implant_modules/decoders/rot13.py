from decoder import Decoder
import codecs


class ROT13(Decoder):
    
    display_name = "ROT-13"
    
    def decode(self, params):
        
        data = params['data']
        
        decoded_data = codecs.decode(data, 'rot_13')
        return decoded_data