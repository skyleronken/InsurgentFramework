from bottle import route, run, template, Bottle, view, TEMPLATE_PATH
import pkgutil
from implant import beacons, commands
from types import ModuleType
from implant.controller import Controller

#########
# UTILS #
#########


def get_module_list(package, parent = None):
    ''' 
    Expects an actual package to be provided
    it will then get all the modules themselves.
    It will also only grab those who inherit from 'parent'
    '''
    modules_list = []
    
    #Get the module's Class name only
    #if isinstance(parent, ModuleType):
    #    parent = ## Need a better way...
    
    prefix = package.__name__ + "."
    
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):

        module_class = Controller.easy_import(package.__name__,modname.split('.')[-1])

        if parent:
            #if the parent is not correct, then skip the add and continue enumerating.
            if module_class.__name__ == parent:
                continue
        
        modules_list.append(module_class)

    return modules_list


#########
# VIEWS #
#########


builder = Bottle()
TEMPLATE_PATH.insert(0,'./c2/web/views')

@builder.route('/')
@builder.route('/builder')
def builder_index():
    return template('builder',node_modules=get_module_list(beacons,'Beacon'),command_modules=get_module_list(commands,'Command'))
    
@builder.route('/builder/create')
def create_settings():
    return template('settings_form')
    
def load_settings():
    pass
    
