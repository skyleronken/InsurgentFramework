from uuid import uuid1

class Order:
    
    node = None
    raw_response = None
    node_type = None
    node_port = None
    node_ip = None
    commands = None
    stop_on_fail = False
    include_cmd_in_response = True
    results = None
    response = None
    uuid = None
    
    
    def __init__(self):
        self.uuid = uuid1()