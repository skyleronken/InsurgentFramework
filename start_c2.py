#!/usr/bin/env python
from bottle import Bottle, run, route, static_file
from c2.web.builder_web import builder

# FormEncode - Form Generator
# Genshi - XML to HTML

if __name__ == '__main__':

    app = Bottle()
    
    @app.route('/src/<filename:path>')
    def fileget(filename):
        return static_file(filename, root='./c2/web/static/')
    
    app.merge(builder)
    
    app.run(host='0.0.0.0', port=8080, debug=True, reloader=True)