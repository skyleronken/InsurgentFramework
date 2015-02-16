
import config

class CommandObject(object):
    
    name = None
    args = None
    
    def __init__(self,data):
        """
        will take Dictionaries with the format {config.CMD_NAME_KEY:"cmd name", config.CMD_ARGS_KEY:"cmd args"}, it will attept to break strings into 
        CommandObjects by splitting on spaces or a non-alphanumeric character defined by being the first character in the string. 
        It will also take Dictionaries and try to create them as {"name":"args"}.
        """
        try:
            if type(data) is str:
                
                #Check to see if this string has spaces, or other possibly delimiting characters.
                if data.isalnum():
                    #its just a singple alphanumeric word. Add it as the command name and thats it.
                    self.name = data
                else:
                    split_char = data[0] # get delimiter character
                    if split_char.isalnum(): # check if its alphanumeric, if so, set split_char to " "
                        split_char = " "
                    split_data = data.split(split_char) # split character along delimeter
                    
                    self.name = split_data.pop(0) # set the name to be the first value, while removing it from the list
                    self.args = split_data # set the args to be the rest of the data
                        
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
        