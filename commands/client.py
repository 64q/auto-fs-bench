#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import json

import bench


def error(reason="Generic error"):
    """Fonction permettant de notifier une erreur au serveur"""
    
    return json.dumps({"command": "error", "returnValue": reason})


def test(params):
    """ TODO TODO TODO Fonction permettant de tester si le client est correctement initialisé"""
    
    mods = bench.modLoad(params["modules"])
    valid = True

    for k in params["modules"]:
        module = mods[k]
        
        if module is None or not module.test():
            valid = False
            
        
    return json.dumps({"command": "test", "returnValue": valid})


def heartbeat():
    """Réponse à un heartbeat"""
    
    return json.dumps({"command": "heartbeat", "returnValue": True})


def run(params):
    """Fonction pour effectuer un test de benchmark"""
    
    output = dict()
    mods = bench.modLoad(params["modules"])
    
    for k in params["modules"]:
        module = mods[k]
        
        if module is None:
            return error()
        else:
            output[k] = bench.modLaunch(module, "run", params["path"], nb=params["times"])

            print "output> ", output[k]
    
    return json.dumps({"command": "run", "returnValue": output})
