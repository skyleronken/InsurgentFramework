import sys
import os
from subprocess import Popen, PIPE

from command import Command

class ShellCommand(Command):
    
    display_name = "Shell Command"
    
    def execute(self, cmd_line):
        
        success = True
        cmd_line = cmd_line.split()
        results = Popen(cmd_line, stdout=PIPE).communicate()[0]
        
        return success, results
        