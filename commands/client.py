#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import json

def error():
    """Fonction permettant de notifier une erreur au serveur"""
    
    return json.dumps({"command": "error"})

def test(params):
    """ TODO TODO TODO Fonction permettant de tester si le client est correctement initialisé"""
    
    for m in params["modules"]:
        pass

def heartbeat():
    """Réponse à un heartbeat"""
    
    return json.dumps({"command": "heartbeat", "returnValue": True})

def run(params):
    """Fonction pour effectuer un test de benchmark"""
    
    output = "Test '%s' effectue, config = %s" % (params["test"], params["conf"])
    
    return json.dumps({"command": "run", "returnValue": output})
