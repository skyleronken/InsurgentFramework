from codec import Codec
import codecs

class ROT13(Codec):
    
    display_name = "ROT-13"
    
    def decode(self, data):

        try:
            decoded_data = codecs.decode(data, 'rot_13')
            return decoded_data
        except Exception, e:
            return data

    def encode(self, params):
        return self.decode(params)