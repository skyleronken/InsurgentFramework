'''
A series of helper functions for command modules
'''
from socket import gethostname, getaddrinfo

def get_ips():
    
    ips =  [i[4][0] for i in getaddrinfo(gethostname(), None)]
    return ips