""" This file contains the variables accessible accross all modules """


DEFAULT_CONFIG_FILE = "settings.xml"

# Settings Parsing Options
NODES_TAG = 'nodes'
NODE_TAG = 'node'
N_TYPE_T = 'type'
N_PORT_T = 'port'
N_HOST_T = 'host'
PARAMS_TAG = 'parameters'
PARAM_TAG = 'parameter'
P_NAME_T = 'name'
BEHAV_TAG = 'behaviors'
MIN_SLEEP_T = 'min_sleep'
MAX_SLEEP_T = 'max_sleep'
ACTIVITY_TAG = 'activity'
DAYS_TAG = 'days'
HOURS_TAG = 'hours'
L_HOUR_T = 'low_hour'
H_HOUR_T = 'high_hour'

# Default Behaviors
MIN_SLEEP_INT = 60 # default
MAX_SLEEP_INT = 60 # default
ACTIVE_DAYS = ('M','T','W','Th','F','Sa','Su') # default
ACTIVE_HOURS = ('0001','2359') # default
NODES = None

CONTINUE_BEACON = True

PROMPT = "[]>"
