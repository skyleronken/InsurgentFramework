import json
from decoder import Decoder

class JSON(Decoder):
    
    display_name = "JSON"
    
    def decode(self, params):
        
        json_data = params['data']
        
        decoded_json = json.loads(json_data)
    
    	return decoded_json