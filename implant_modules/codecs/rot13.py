from codec import Codec
import codecs


class ROT13(Codec):
    
    display_name = "ROT-13"
    
    def decode(self, params):
        
        data = params['data']
        
        decoded_data = codecs.decode(data, 'rot_13')
        return decoded_data
        
    def encode(self, params):
        pass