import sys
import urllib2
import os

from command import Command, URL_KEY, D_PATH_KEY, D_NAME_KEY

class HttpDownload(Command):
    
    display_name = "HTTP Download"
    
    def execute(self, params):
        
        self.url = params[URL_KEY]
        self.dst_path = params.get(D_PATH_KEY) or os.getcwd()
        self.save_as_name = params.get(D_NAME_KEY) or self.url.split('\\')[-1]  # get last portion of URL as download name

    	f = urllib2.urlopen(self.url)
    
    	full_file_path = self.dst_path + os.pathsep + self.save_as_name
    
    	with open(full_file_path, "wb") as code:
    		code.write(f.read())