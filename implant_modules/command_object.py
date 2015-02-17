
import config

class CommandObject(object):
    
    name = None
    args = None
    success = None
    results = None
    delimeter = None
    args_delimeter = None
    
    def __init__(self,data = None):
        """
        will take Dictionaries with the format {config.CMD_NAME_KEY:"cmd name", config.CMD_ARGS_KEY:"cmd args"}, it will attept to break strings into 
        CommandObjects by splitting on spaces or a non-alphanumeric character defined by being the first character in the string. 
        It will also take Dictionaries and try to create them as {"name":"args"}.
        Examples:
        - {config.CMD_NAME_KEY:"cmd_name", config.CMD_ARGS_KEY:{args}}
        - {"cmd":"args"}
        - "cmd_name"
        - |cmd_name|arg1|arg2|arg3 (Where | is arbitrary non-alphanumerics, will split on whitespace as default)
        - |cmd_name|^key1^value1|key2&value2 ( Where | and ^ are arbitrary non-alphanumerics, and ^ is NOT whitespace)
        """
        if (data is not None):
            try:
                if type(data) is str:
                    
                    #Check to see if this string has spaces, or other possibly delimiting characters.
                    if data.isalnum():
                        #its just a singple alphanumeric word. Add it as the command name and thats it.
                        self.name = data
                    else:
                        self.delimeter = data[0] # get delimiter character
                        if self.delimeter.isalnum(): # check if its alphanumeric, if so, set split_char to " "
                            self.delimeter = " "
                        split_data = data.split(self.delimeter) # split character along delimeter
                        
                        self.name = split_data.pop(0).strip() # set the name to be the first value, while removing it from the list
                        
                        split_data = [ x.strip() for x in split_data ] # remove trailing and leading white space that may exist
                        
                        if split_data[0][0].isalnum(): # is there an args delimeter set?
                            self.args = split_data.strip # Nope, set the args to be the rest of the data
                        else:
                            self.args_delimeter = split_data[0].pop(0) # Yes! Save it and remove it.
                            self.args = {}
                            for arg in split_data: # loop through the initally delimeted data
                                s_arg = arg.split(self.args_delimeter) # split it based on the sub delimeter
                                self.args[s_arg[0]] = s_arg[1] # Add it to a dictionary
                            
                elif type(data) is dict:
                    
                    self.name = data.get(config.CMD_NAME_KEY, None)
                    self.args = data.get(config.CMD_ARGS_KEY, None)
    
                    if self.name is None:
                        for name, args in data.items(): # unpack the dict
                            self.name = name
                            self.args = args
    
                else:
                    print "Could not construct using %s" % data
                    raise
            except Exception, e:
                print "%s %s" % (e, data)
                raise
        