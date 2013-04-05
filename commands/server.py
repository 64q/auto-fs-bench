#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import core.transmission, core.utils, core.errors


def test(host, port, test):
    """Fonction permettant de vérifier que le test est valide sur le client"""
    
    config = core.utils.load_config_test(test)
    modules = config.modules

    try:
        result = core.transmission.send_to_client(host, port, "test", params={"modules": modules})

        return result["returnValue"]
    except core.errors.ClientTimeoutError:
        return False


def heartbeat(host, port):
    """Fonction permettant d'envoyer des msgs de type heartbeat"""
    
    try:
        result = core.transmission.send_to_client(host, port, "heartbeat", timeout=0.1)

        return result["returnValue"]
    except core.errors.ClientTimeoutError:
        return False


def run(host, port, conf):
    """Fonction permettant d'exécuter un test de benchmark"""
    
    return core.transmission.send_to_client(host, port, "run", params=conf)