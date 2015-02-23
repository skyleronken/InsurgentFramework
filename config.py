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
MODULES_TAG = 'modules'
MOD_T = 'module'
BEACONS_MOD_T = 'beacons'
COMMANDS_MOD_T = 'commands'
DECODERS_MOD_T = 'decoders'
ENCODERS_MOD_T = 'encoders'
RESPONDERS_MOD_T = 'responders'
MOD_TYPE_T = 'type'
MOD_ORDER_T = 'order'

# Controller keys and indecies
CMD_SUCC_KEY = 'success'
CMD_RES_KEY = 'results'
CMD_NAME_KEY = 'command'
CMD_ARGS_KEY = 'args'
NODE_IP_KEY = 'node'
NODE_PORT_KEY = 'port'
BEACON_TYPE_IND = 0
PARAMS_IND = 1
CMD_SUCCESS_IND = -2 # These are used when the CommandObject is parsed and transformed into non-KVP delimeted lists.
CMD_RESULTS_IND = -1

# Controller paths to modules
MODULE_PATH = 'implant'
BEACON_MODULE = 'beacons'
COMMAND_MODULE = 'commands'
DECODER_MODULE = 'codecs'
ENCODER_MODULE = 'codecs'
RESPONDER_MODULE = 'beacons'
BEACON_PKG = MODULE_PATH + '.' + BEACON_MODULE
COMMAND_PKG = MODULE_PATH + '.' + COMMAND_MODULE
DECODER_PKG = MODULE_PATH + '.' + DECODER_MODULE
ENCODER_PKG = MODULE_PATH + '.' + ENCODER_MODULE
RESPONDER_PKG = MODULE_PATH + '.' + RESPONDER_MODULE

# Parent ABC
BEACON_ABC = 'beacon'
COMMAND_ABC = 'command'
DECODER_ABC = 'codec'
ENCODER_ABC = 'codec'
RESPONDR_ABC = 'beacon'


# Default Behaviors
MIN_SLEEP_INT = 60 # default
MAX_SLEEP_INT = 60 # default
ACTIVE_DAYS = ('M','T','W','Th','F','Sa','Su') # default
ACTIVE_HOURS = ('0001','2359') # default

# Modules
NODES = None
BEACONS = None
DECODERS = None
COMMANDS = None
ENCODERS = None
RESPONDERS = None

# Flags
CONTINUE_BEACON = True

# Prompts
PROMPT = "[]>"
PROMP_SEP = "->"
PROMP_BASE = "[Controller"
PROMP_END = "]>"
BASIC_PROMPT = PROMP_BASE + PROMP_END
BEAC_PROMPT = PROMP_BASE + PROMP_SEP + 'Beaconer' + PROMP_END
DEC_PROMPT = PROMP_BASE + PROMP_SEP + 'Decoder' + PROMP_END
CMD_PROMPT = PROMP_BASE + PROMP_SEP + 'Commander' + PROMP_END
ENC_PROMPT = PROMP_BASE + PROMP_SEP + 'Encoder' + PROMP_END
RESP_PROMPT = PROMP_BASE + PROMP_SEP + 'Responder' + PROMP_END
COD_PROMPT = None
