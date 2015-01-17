import sys
import os
from subprocess import Popen, PIPE

from command import Command

class TestCommand(Command):
    
    display_name = "Test Command"
    
    def execute(self, cmd_line):
        
        print 'Test Command: %s' % (cmd_line)
        return (True, 'Results')
        