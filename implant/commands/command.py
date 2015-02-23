from abc import ABCMeta

# Central location to store globals. Allows us to change plain text data into hex or alpha numeric names, etc for params.
D_PORT_KEY = 'd_port'
D_HOST_KEY = 'd_host'
RAND_SRC_KEY = 'rand_src'
URL_KEY = 'url'
D_PATH_KEY = 'dst_path'
D_NAME_KEY = 'dst_name'
 

class Command:
    __metaclass__ = ABCMeta
    
    display_name = "Abstract Command"
    
    def name(self):
        return self.display_name
    
    def execute(self, arguments):
        
        #
        # The controller will call this method on all Commands. The arguments will contain the parsed parameters provided by the C2 node.
        #
        # The method should return:
        #   - Non-terminating threads (i.e, indefinite tasks)
        #   - Success / Failure
        #   - Success outpu / Failure details
        #
        #   I am still debating whether or not to pass these back in a dictionary. It is likely that I will.
        #
        
        while False:
                yield None