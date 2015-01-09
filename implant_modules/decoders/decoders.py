#!/usr/bin/env python

#
# These functions will decode the responses from the LP nodes.
#
# The application controller that implements these functions should check to see if the 'data' being passed is iterable. 
# If it is, each iteration needs to be ran through the function as the 'data', with the result being reassembled by the
# application controller.
#

import time
import codecs
import base64
import json
import sys

def decode_base64(self, data):

	decoded_data = base64.urlsafe_b64decode(data)
	return decoded_data

def decode_json(self, data):

	decoded_json = json.loads(json_data)

	decoded_data = dict()
	for key in decoded_json:
		commands[d_key] = d_val

	return decoded_data

def decode_rot13(self, data):
	
	decoded_data = codecs.decode(data, 'rot_13')
	return decoded_data

def decode_xor(self, data):
	pass

def decode_jpeg(self, data):
	pass
