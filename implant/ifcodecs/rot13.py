from implant.ifcodecs.codec import Codec
import codecs as py_codecs

class ROT13(Codec):
    
    display_name = "ROT-13"
    
    def decode(self, data):

        try:
            decoded_data = py_codecs.decode(data, 'rot_13')
            return decoded_data
        except Exception, e:
            return data

    def encode(self, params):
        return self.decode(params)