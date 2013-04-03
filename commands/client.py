#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import json

def error():
    return json.dumps({"command": "error"})

def heartbeat():
    return json.dumps({"command": "heartbeat", "returnValue": True})

def run(params):
    output = "Test '%s' effectue, config = %s" % (params["test"], params["conf"])
    
    return json.dumps({"command": "run", "returnValue": output})
