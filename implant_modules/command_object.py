
import config
import copy

FULL_DICT = 1
SHORT_DICT = 2
SIMP_STRING = 3
DELIM_LIST = 4
DELIM_DICT = 5

class CommandObject(object):
    
    name = None
    args = None
    success = None
    results = None
    delimeter = None
    args_delimeter = None
    format_type = None
    
    def __init__(self,data = None):
        """
        will take Dictionaries with the format {config.CMD_NAME_KEY:"cmd name", config.CMD_ARGS_KEY:"cmd args"}, it will attept to break strings into 
        CommandObjects by splitting on spaces or a non-alphanumeric character defined by being the first character in the string. 
        It will also take Dictionaries and try to create them as {"name":"args"}.
        Format Types:
        1 - {config.CMD_NAME_KEY:"cmd_name", config.CMD_ARGS_KEY:{args}}
        2 - {"cmd":"args"}
        3 - "cmd_name"
        4 - |cmd_name|arg1|arg2|arg3 (Where | is arbitrary non-alphanumerics, will split on whitespace as default)
        5 - |cmd_name|^key1^value1|key2&value2 ( Where | and ^ are arbitrary non-alphanumerics, and ^ is NOT whitespace)
        
        The constructor will attempt to do a few things:
        - extract Results and Success data. So do not send params with those keys.
        - make sure that the CommandObject's args value is a dictionary. So it will convert a list into a dictionary, using indecies as keys
        but it will also take strings and single datatypes and add them into a dictionary with the key of '0'. So for all intents and purposes
        the args will make it transparent to the command modules whehter or not its a list or a dictionary.
        """
        if (data is not None):
            try:
                if type(data) is str:
                    
                    #Check to see if this string has spaces, or other possibly delimiting characters.
                    if data.isalnum():
                        #its just a singple alphanumeric word. Add it as the command name and thats it.
                        self.name = data
                        self.format_type = SIMP_STRING
                    else:
                        self.delimeter = data[0] # get delimiter character
                        if self.delimeter.isalnum(): # check if its alphanumeric, if so, set split_char to " "
                            self.delimeter = " "
                        split_data = data.split(self.delimeter) # split character along delimeter
                        
                        self.name = split_data.pop(0).strip() # set the name to be the first value, while removing it from the list
                        
                        split_data = [ x.strip() for x in split_data ] # remove trailing and leading white space that may exist
                        
                        if split_data[0][0].isalnum(): # is there an args delimeter set?
                            self.args = split_data.strip # Nope, set the args to be the rest of the data
                            self.format_type = DELIM_LIST
                        else:
                            self.args_delimeter = split_data[0].pop(0) # Yes! Save it and remove it.
                            self.args = {}
                            for arg in split_data: # loop through the initally delimeted data
                                s_arg = arg.split(self.args_delimeter) # split it based on the sub delimeter
                                self.args[s_arg[0]] = s_arg[1] # Add it to a dictionary
                                
                            self.format_type = DELIM_DICT
                            
                elif type(data) is dict:
                    
                    self.name = data.get(config.CMD_NAME_KEY, None)
                    self.args = data.get(config.CMD_ARGS_KEY, None)
                    self.results = data.get(config.CMD_RES_KEY, None) # check to see if this is a parsed result
                    self.success = data.get(config.CMD_SUCC_KEY, None) # check to see if this is a parsed result
    
                    self.format_type = FULL_DICT
                    if self.name is None:
                        for name, args in data.items(): # unpack the dict
                            self.name = name
                            self.args = args
                        self.format_type = SHORT_DICT
    
                else:
                    print "Could not construct using %s" % data
                    raise
            except Exception, e:
                print "%s %s" % (e, data)
                raise
            
            # if args is not a dict, add it to a dict.
            if type(self.args) is not dict:
                
                if type(self.args) is list:
                    d = {}
                    for i in len(self.args):
                        d[i] = self.args[i]
                    
                    self.args = d
                    
                else:
                    temp_args = self.args
                    self.args = {}
                    self.args[0] = temp_args
            
            # If it so happens that success and results are set, remove from args and add them to the command object
            if config.CMD_SUCC_KEY in self.args: 
                self.success = self.args.pop(config.CMD_SUCC_KEY, None)
                        
            if config.CMD_RES_KEY in self.args:
                self.results = self.args.pop(config.CMD_RES_KEY, None)
    
    def to_string(self, short=False):
        
        # Return simple command name string
        if self.args is None:
            return str(self.name)
        
        # return dictionaries
        elif self.delimeter is None:
            dictionary = {}
            if short:
                dictionary[self.name] = self.args
            else:
                dictionary[config.CMD_NAME_KEY] = self.name
                dictionary[config.CMD_ARGS_KEY] = self.args
            
            return str(dictionary)
        
        # returns a string with listed arguments
        elif type(self.args) is list or self.args_delimeter is None:
            ret_str = str(self.delimeter)
            ret_str += str(self.name)
            for arg in self.args:
                ret_str += str(self.delimeter)
                ret_str += str(arg)
            return ret_str
        
        # returns a string with KVP arguments
        elif type(self.args) is dict and self.args_delimeter is not None:
            ret_str = str(self.delimeter)
            ret_str += str(self.name)
            ret_str += str(self.delimeter)
            ret_str += str(self.args_delimeter)
            for key, val in self.args.items():
                ret_str += str(key)
                ret_str += str(self.args_delimeter)
                ret_str += str(val)
                ret_str += str(self.delimeter)
            ret_str = ret_str.rstrip(self.delimeter) # remove last delimeter
            
            return ret_str
        else:
            return None
            
    def get_results(self):
        
        sc = copy.deepcopy(self)
        res_string = ""

        if sc.format_type == SIMP_STRING or sc.format_type == DELIM_LIST:
            
            if sc.delimeter is None:
                sc.delimeter = " " # This is why its bad to use the SIMP_STRING format; results will contain spaces, and parsing will be a pain.
            else:
                res_string += str(sc.delimeter)
                
            res_string += str(sc.name)

            if len(sc.args) > 0:
                for arg in sc.args:
                    res_string += str(sc.delimeter)
                    res_string += str(sc.arg)
            
            res_string += str(sc.delimeter)
            res_string += str(sc.success)
            res_string += str(sc.delimeter)
            res_string += str(sc.results)

        elif sc.format_type == DELIM_DICT:
            
            res_string += str(sc.delimeter)
            res_string += str(sc.name)
            
            res_string += str(sc.delimeter)
            res_string += str(sc.args_delimeter)
            
            for key, val in sc.args:
                res_string += str(key)
                res_string += str(sc.args_delimeter)
                res_string += str(val)
                res_string += str(sc.delimeter)
                
            res_string += str(config.CMD_SUCC_KEY)
            res_string += str(sc.args_delimeter)
            res_string += str(sc.success)
            
            res_string += str(sc.delimeter)
            
            res_string += str(config.CMD_RES_KEY)
            res_string += str(sc.args_delimeter)
            res_string += str(sc.results)
            
        elif sc.format_type == SHORT_DICT:
            
            d = {}
            sc.args[config.CMD_SUCC_KEY] = sc.success
            sc.args[config.CMD_RES_KEY] = sc.results
            d[sc.name] = sc.args
            
            res_string = str(d)
        
        elif sc.format_type == FULL_DICT:
            
            d = {}
            d[config.CMD_NAME_KEY] = sc.name
            d[config.CMD_ARGS_KEY] = sc.args
            d[config.CMD_SUCC_KEY] = sc.success
            d[config.CMD_RES_KEY] = sc.results
            
            res_string = str(d)

        return res_string