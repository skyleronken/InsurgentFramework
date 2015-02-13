import config
import xml.etree.ElementTree as ET
from sys import exit

def get_xml(config_filename):
    
    """ 
    Take a filename, and attempts to parse it into an XML Tree Element
    """
    
    try:
        xmltree = ET.parse(config_filename)
        xmlroot = xmltree.getroot()
    except IOError, io:
        print '%s ERROR: Issue getting file \'%s\'. Make sure it exists at the appropriate path.' % (config.PROMPT, config_filename)
        exit()
    except Exception, e:
        raise e
        
    return xmlroot

def parse_nodes(xml):
    
    """
    Parse the XML 'Nodes' element for its children 'node' elements. Use these define where to beacon to.
    """
    
    nodes_list = []
    # Get all <node> elements within <nodes>
    for n in xml.findall(config.NODE_TAG):
        
        try:
            # get the node type, i.e http_get, etc
            n_type = n.attrib[config.N_TYPE_T]
        
            # create a dictionary containing the ip/host and port. the rest of the parameters are provided later. This is the bare minimum.
            n_dict = {}
            n_dict[config.NODE_PORT_KEY] = n.find(config.N_PORT_T).text
            n_dict[config.NODE_IP_KEY] = n.find(config.N_HOST_T).text
            
        except:
            print '%s Nodes must provide a type, host/ip and port at minimum' % (config.PROMPT)
            raise
        
        # Get the rest of the variable number and variably named arguments. Parser doesn't need to be aware of what these do; the module
        # itself will know what to do with them.
        for param in n.find(config.PARAMS_TAG).findall(config.PARAM_TAG):
            n_dict[param.get(config.P_NAME_T)] = param.text
        
        nodes_list.append((n_type,n_dict))
        
    if len(nodes_list) > 0:
        config.NODES = nodes_list
        return True
    else:
        return False
        
def parse_activity_rules(xml):
    
    """
    Parses the beaconing behavior settings from the XML settings file. Current beaconing activity behaviors:
    - Min and Max Sleep time
    - Acceptable days to beacon on
    - Acceptable time range to beacon during
    """
    
    min_s = xml.find(config.MIN_SLEEP_T)
    max_s = xml.find(config.MAX_SLEEP_T)
    
    # Get the min and max sleep time for randomly calculated sleep intervals between beaconing
    if min_s is not None and max_s is not None:
        config.MIN_SLEEP_INT = int(min_s.text)
        config.MAX_SLEEP_INT = int(max_s.text)
    
    # create list of days of the week that the bot should beacon on    
    days = []
    for day in xml.findall(config.DAYS_TAG):
        days.append(day.text)
    
    if len(days) > 0:
        config.ACTIVE_DAYS = days
    
    # Get the hour range from which beaconing should occur. HHMM format. This can go over the 24-hour mark to indicate
    # overnight times.
    hours = xml.find(config.HOURS_TAG)
    low_hour = hours.find(config.L_HOUR_T)
    high_hour = hours.find(config.H_HOUR_T)
    if low_hour is not None and high_hour is not None:
        config.ACTIVE_HOURS = (int(low_hour.text), int(high_hour.text))

def parse_behaviors(xml):
    """
     Run the parsers for all behaviors settings.
    """
    try:
        parse_activity_rules(xml.find(config.ACTIVITY_TAG))
        
    except:
        print '%s Error parsing behaviors' % (config.PROMPT)
        raise

def parse_abstract_type_module(xml):
    """
    this function is called to parse the modules within the different module tags
    """
    parsed_modules = []
    # get all module objects
    for module in xml.findall(config.MOD_T):
        mod_type = module.find(config.MOD_TYPE_T).text
        mod_order = int(module.attrib.get(config.MOD_ORDER_T, -1)) # if no order attribute is defined, default to False.
        
        # if there is an order defined, put it into the list at the appropriate index. 
        # Order of definitions should'nt matter as long as you start at 1, not 0 index.
        if mod_order:
            parsed_modules.insert(mod_order,mod_type)
        else:
            parsed_modules.append(mod_type)
    return parsed_modules
    
def parse_beacons(xml):
    """ parses beacon modules """
    beacons = parse_abstract_type_module(xml)
    config.BEACONS = beacons

def parse_decoders(xml):
    """ parses decoders"""
    
    decoders = parse_abstract_type_module(xml)
    config.DECODERS = decoders

def parse_commands(xml):
    """ parses commands """
    
    commands = parse_abstract_type_module(xml)
    config.COMMANDS = commands

def parse_encoders(xml):
    """ parses encoders """
    encoders = parse_abstract_type_module(xml)
    config.ENCODERS = encoders

def parse_responders(xml):
    """ pares responders """
    
    responders = parse_abstract_type_module(xml)
    config.RESPONDERS = responders
    
def parse_modules(xml):
    """
    Run the parsers for all of the modules.
    """
    try:
        parse_beacons(xml.find(config.BEACONS_MOD_T))
        parse_decoders(xml.find(config.DECODERS_MOD_T))
        parse_commands(xml.find(config.COMMANDS_MOD_T))
        parse_encoders(xml.find(config.ENCODERS_MOD_T))
        parse_responders(xml.find(config.RESPONDERS_MOD_T))
    except:
        print '%s Error parsing modules' % (config.PROMPT)
        raise