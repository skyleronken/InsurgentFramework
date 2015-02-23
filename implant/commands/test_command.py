import sys
import os
from subprocess import Popen, PIPE

from command import Command

class TestCommand(Command):
    """
    This class does nothing but return a True result and string
    """
    display_name = "Test Command"
    
    def execute(self, cmd_line):
        
        return (True, 'Results')
        