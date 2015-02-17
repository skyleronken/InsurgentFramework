#!/usr/bin/env python

from argparse import ArgumentParser
from controller import Controller
from implant_modules.command_object import CommandObject
import config_parser
import config
import sys
import pprint
from json import dumps, loads

class Translator:
    
    def __init__(self, xml):
        self.xml = xml.find(config.MODULES_TAG)
        decoders_types = config_parser.parse_decoders(self.xml)
        encoders_types = config_parser.parse_encoders(self.xml)
        if len(encoders_types) < 1:
            encoders_types = reversed(decoders_types)
        self.controller = Controller([], [], decoders_types, encoders_types, [])
    
    def encode_for_sending(self, data):
        """
        This function will run the setting's 'decoding' chain in reverse, invoking the encoding methods.
        This is necessary since some settings may choose to use different encoders for their responses 
        than they do for their decoding of orders.
        """
        store_encoders = self.controller.encoder_list
        self.controller.encoder_list = reversed(self.controller.decoder_list)
        results = self.controller.handle_encode(data)
        self.controller.encoder_list = store_encoders
        return results
    
    def decode_for_receiving(self, data):
        """
        This function will run the setting's 'encoding' chain in reverse, invoking the decodeing methods.
        """
        store_decoders = self.controller.decoder_list
        self.controller.decoder_list = reversed(self.controller.encoder_list)
        results = self.controller.handle_decode(data)
        self.controller.decoder_list = store_decoders
        return results
    
    def decode_as_bot(self, data):
        """ 
        runs the decoders exactly as the settings lay them out
        """
        return self.controller.handle_decode(data)

    def encode_as_bot(self, data):
        """
        runs the encoders exactly as the settings lay them out
        """
        return self.controller.handle_encode(data)
        
    def parse_to_cmd_objs(self, data):
        """
        loops through data and convert its to CommandObjects
        """
        return Controller.recursive_convert_to_cmd_objects(data)

def print_header():
    header = """
          _______                  _       _             
         |__   __|                | |     | |            
            | |_ __ __ _ _ __  ___| | __ _| |_ ___  _ __ 
            | | '__/ _` | '_ \/ __| |/ _` | __/ _ \| '__|
            | | | | (_| | | | \__ | | (_| | || (_) | |   
            |_|_|  \__,_|_| |_|___|_|\__,_|\__\___/|_|   
    """
    print header

def print_menu():
    menu = """
        Options:
        1) Encode for sending
        2) Decode a response
        3) Decode as the bot would
        4) Encode as the bot would
        5) Exit
        
    """
    print menu
      
def main(settings_file, full_decode):
    xml = config_parser.get_xml(settings_file)
    translator = Translator(xml)
    
    print_header()
    loop = True
    while loop:
        print_menu()
        choice = input("%s Enter your choice: " % config.PROMPT)
        choice = int(choice)
        
        if choice >= 1 and choice <= 4:
            data = raw_input("%s Input data: \n" % config.PROMPT)

        if choice == 1:
            result = translator.encode_for_sending(data)
        elif choice == 2:
            result = translator.decode_for_receiving(data)
        elif choice == 3:
            result = translator.decode_as_bot(data)
        elif choice == 4:
            result = translator.encode_as_bot(data)
        elif choice == 5:
            loop = False
            return 0
        else:
            result = "%s I don't understand" % config.PROMPT
            continue
            
        print "\n\nResult:\n"
        
        if full_decode and (choice == 2 or choice == 3):
            if type(result) is tuple:
                success, body = result
            results_as_obj = translator.parse_to_cmd_objs(body)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(results_as_obj)
        else:
            print result

if __name__ == "__main__":
    
    ap = ArgumentParser(prog='translator',description='Encode commands and decode responses interactively')
    ap.add_argument('-s','--settings', dest='settings_file',nargs='?', default='settings.xml', required=True, help="The absolute path of the settings XML file from which you created your bot.")
    ap.add_argument('-f','--full', dest='full_decode', action='store_true', required=False, help="When decoding, fully decode in Command Objects.")
    parsed_args = ap.parse_args()
    
    try:
        main(parsed_args.settings_file, parsed_args.full_decode)
        sys.exit(0)
    except (KeyboardInterrupt, SystemExit):
        print config.PROMPT + " Exiting"
        sys.exit()