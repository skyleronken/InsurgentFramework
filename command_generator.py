#!/usr/bin/env python

from argparse import ArgumentParser
from implant.command_object import CommandObject, ft_dict
from implant.controller import Controller
import config_parser
import config
import sys
from subprocess import Popen, PIPE, STDOUT

def print_header():
    header = """
           _____               _    _____            
          / ____|             | |  / ____|           
         | |     _ __ ___   __| | | |  __  ___ _ __  
         | |    | '_ ` _ \ / _` | | | |_ |/ _ \ '_ \ 
         | |____| | | | | | (_| | | |__| |  __/ | | |
          \_____|_| |_| |_|\__,_|  \_____|\___|_| |_|
                                             
    """
    print header

def get_command_name(commands_list = None):
    
    if commands_list:
        menu = "Commands:\n\n"
        for i, cmd in enumerate(commands_list):
            mod = Controller.easy_import(config.COMMAND_PKG, cmd)
            menu += "[%i] %s\n" % (i, mod.display_name)
        print menu
        select_text = "Enter your selection: "
    
        choice = input(select_text)
        return commands_list[int(choice)]
    else:
        choice = input("Enter the command name: ")
        return choice

def print_current_params(params):
    
    if params is not None:
        print "Current Parameters:\n"
        for k, v in params.items():
            print "[%s] %s" % (k, v)

def set_new_param(args):
    
    key = raw_input("Enter the key [blank for list-like index]: ")
    val = raw_input("Enter the value: ")
    
    if key is None or key is "":
        key = len(args)
        
    args[str(key)] = val

def remove_param(args):
    
    print_current_params(args)
    choice = raw_input("Enter key to delete: ")
    del args[str(choice)]
    
def set_format_type(ft):
    
    if ft is not None:
        print "\nCurrent Format Type is: %s" % (ft_dict[int(ft)])
    
    print "\nAvailable Formats:"
    for k, v in ft_dict.items():
        print "[%s] %s" % (k, v)
        
    choice = raw_input("\nSelect Format: ")
    return int(choice)
    
def set_delimeter(deli):
    
    print "\nCurrent Delimeter is: %s \n" % (deli)

    choice = raw_input("Select Delimeter: ")
    if len(choice) == 0:
        choice = None
    return choice
    
def set_args_delimeter(deli):

    print "\nCurrent Args Delimeter is: %s \n" % (deli)

    choice = raw_input("Select Args Delimeter: ")
    if len(choice) == 0:
        choice = None
    return choice
    
def print_main_menu():
    
    menu = """
    
    [1] Set Command
    [2] Add argument
    [3] Delete argument
    [4] Show current arguments
    [5] Set Format Type
    [6] Set Delimiter
    [7] Set Args Delimeter
    [8] Show CommandObject Representation
    [9] Print Constructed Command String
    [10] Sanity Check Constructed String
    [11] Run through Translator
    [12] Exit
    
    """
    
    print menu
    choice = input("Enter your selection: ")
    return choice

def main(settings = None):
    
    com_obj = CommandObject()
    
    print_header()
    
    cont = True
    while cont:
        choice = print_main_menu()
        
        if choice == 1:
            if settings is not None:
                xml = config_parser.get_xml(settings)
                mod_xml = xml.find(config.MODULES_TAG)
                commands_list = config_parser.parse_commands(mod_xml)
            else:
                commands_list = None
            
            com_obj.name = get_command_name(commands_list)
        elif choice == 2:
            set_new_param(com_obj.args)
        elif choice == 3:
            remove_param(com_obj.args)
        elif choice == 4:
            print_current_params(com_obj.args)
        elif choice == 5:
            com_obj.format_type = set_format_type(com_obj.format_type)
        elif choice == 6:
            com_obj.delimeter = set_delimeter(com_obj.delimeter)
        elif choice == 7:
            com_obj.args_delimeter = set_args_delimeter(com_obj.args_delimeter)
        elif choice == 8:
            print com_obj.__repr__()
        elif choice == 9:
            print com_obj.to_string()
        elif choice == 10:
            str_ver = com_obj.to_string()
            test_obj = CommandObject(str_ver)
            print "Sanity Checked Object. Check for validity: \n"
            print test_obj.__repr__()
        elif choice == 11:
            p = Popen(["python","translator.py","-s",settings,"-c1"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            results = p.communicate(input=b'%s' % (com_obj.to_string()))[0]
            results = results.decode()
            results = results.splitlines()
            success, results = eval(results[-2])
            
            print "Success: %r" % success
            print "Encoded Command: %s" % results
            
        elif choice == 12:
            cont = False
        else:
            print "Incorrect option!"
        
if __name__ == "__main__":
    
    ap = ArgumentParser(prog='command_generator',description='Interactive console for generating commands.')
    ap.add_argument('-s','--settings', dest='settings_file',nargs='?', default='settings.xml', required=False, help="The absolute path of the settings XML file from which you created your bot.")
    parsed_args = ap.parse_args()
    
    try:
        main(parsed_args.settings_file)
        sys.exit(0)
    except (KeyboardInterrupt, SystemExit):
        print config.PROMPT + " Exiting"
        sys.exit()