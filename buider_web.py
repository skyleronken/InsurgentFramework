#!/usr/bin/env python

#http://bottlepy.org/docs/0.12/tutorial.html#generating-content
#http://bottlepy.org/docs/0.11/stpl.html

from bottle import route, run, template, Bottle

builder = Bottle()

@builder.route('/')
@builder.route('/builder')
@builder.route('/builder/<name>')
def builder_index(name=None):
    return template('<b>Hello {{name}}</b>!', name=name)
    
run(builder, host='0.0.0.0', port=8080, debug=True)
