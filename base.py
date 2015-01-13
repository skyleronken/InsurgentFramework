#!/usr/bin/env python

from controller import Controller
import time
from random import randint

# TODO:
# - Prevent replay
# - Add active day and active hour calculation to calculate_sleep()
#

MIN_SLEEP_INT = 60
MAX_SLEEP_INT = 600
ACTIVE_DAYS = ('M','T','W','Th','F','Sa','Su')
ACTIVE_HOURS = ('0001','2359')

# global flag
continue_beacon = True

def calculate_sleep():

    #cur_time = time.ctime()
    sleep_time = 0

    sleep_time += randint(MIN_SLEEP_INT,MAX_SLEEP_INT)
    
    return sleep_time
    

def start_beacon_loop(controller):
    
    while continue_beacon:
        
        controller.beacon()
        time.sleep(calculate_sleep())
        
    return True
                

def main():
    
    controller = Controller()
    
    start_beacon_loop(controller)

if __name__ == "__main__":
    main()
