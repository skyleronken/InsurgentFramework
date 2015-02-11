import config
import xml.etree.ElementTree as ET
from controller import NODE_PORT_KEY, NODE_IP_KEY

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
            n_dict[NODE_PORT_KEY] = n.find(config.N_PORT_T).text
            n_dict[NODE_IP_KEY] = n.find(config.N_HOST_T).text
            
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
        print config.NODES
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
    
    return True