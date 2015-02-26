import httplib
from socket import error as socket_error
from beacon import Beacon

NODE_KEY = 'node'
PATH_KEY = 'path'
PORT_KEY = 'port'

class HttpGet(Beacon):

    display_name = "HTTP Download"
    index = {NODE_KEY:"IP/Host of server",PATH_KEY:"Path of file/script to request",PORT_KEY:"Port server is listening on"}
    
    
    def agnosticize(self, response):
        
        # chomp the last crlf from http
        clean_response = response.rstrip('\n')
        return clean_response
    
    def beacon(self,arguments):
        success = True
        
        node = arguments.get(NODE_KEY)
        path = arguments.get(PATH_KEY)
        port = arguments.get(PORT_KEY)
        timeout = arguments.get('timeout', 8) # Should this be passed? Probably not...
        
        conn = httplib.HTTPConnection(node, port, timeout=timeout)
        conn.request("GET", path)
        response = conn.getresponse()

        if response.status != httplib.OK:
			raise httplib.HTTPException

        data = response.read()
        conn.close()
        
        return (success, self.agnosticize(data))

    def send_response(self, arguments, results):
	    print "Responding!"
	    success = True
	    node = arguments.get('node')
	    path = arguments.get('path')
	    port = arguments.get('port')
	    timeout = arguments.get('timeout',8)
	    
	    conn = httplib.HTTPConnection(node, port, timeout=timeout)
	    conn.request("GET",path + "?" + results)
	    response = conn.getresponse()
	    if response.status != httplib.OK:
	        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	        conn.request("POST", path, results, headers)
	        response = conn.getresponse()
	        
	    conn.close()
	    return success
