from bottle import route, run, template, Bottle, view, TEMPLATE_PATH

builder = Bottle()
TEMPLATE_PATH.insert(0,'./c2/web/views')

@builder.route('/')
@builder.route('/builder')
def builder_index():
    return template('builder')
    
@builder.route('/builder/create')
def create_settings():
    return template('settings_form')
    
def load_settings():
    pass
    
