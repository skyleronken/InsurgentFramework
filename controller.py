#!/usr/bin/env python

#
# This is the application controller that manages the calls through all the different types of modules
#

# TODO:
#
# - Parse XML to build mappings
#

class Controller:
    
    beacon_map = {}
    decoder_map = {}
    command_map = {}
    response_map = {}
    
    def __init__(self):
        self.build_handlers()
        
    
    def build_handlers(self):
        # this function is used by the constructor to setup the dictionaries with the command to command object mapping.
        
        # this is temporary. In the long run should read in XML to parse all mappings.
        # Pass in strings? possible to avoid object types to save the headache of dynamic imports? Makes hard part just retrieving class by reflection, rather than reference.
        pass
    
    def handle_beacon(self):
        pass
    
    def handle_decode(self, encoded_data):
        pass
    
    def handle_command(self, command, params):
        pass
    
    def handle_response(self, results):
        pass
    
    def handle(self):
        
        # Send command to beacon handler
        success, encoded_data = self.handle_beacon()
        
        # Send response to decoders
        success, decoded_data = self.handle_decode(encoded_data)
        
        # Process command
        command, params = decoded_data
        success, results = self.handle_command(command, params)
        
        # Send response
        success = self.handle_response(results)
    
    def beacon(self):
        # facade
        self.handle()
    
    