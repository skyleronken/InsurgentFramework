import json
from codec import Codec

class JSON(Codec):
    
    display_name = "JSON"
    
    def decode(self, params):
        
        json_data = params['data']
        
        decoded_json = json.loads(json_data)
    
    	return decoded_json
    	
    def encode(self, params):
        pass