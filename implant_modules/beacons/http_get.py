import httplib
from socket import error as socket_error
from beacon import Beacon

class HttpGet(Beacon):

    display_name = "HTTP Download"
    
    def agnosticize(self, response):
        return response
    
    def beacon(self,arguments):
        success = True
        
        node = arguments.get('node')
        path = arguments.get('path')
        timeout = arguments.get('timeout') # Should this be passed? Probably not...
        
        conn = httplib.HTTPConnection(node, timeout=timeout)
        conn.request("GET", path)
        response = conn.getresponse()
        
        if response.status != httplib.OK:
			raise httplib.HTTPException

        data = response.read()
        conn.close()
        
        return (success, self.agnosticize(data))

	