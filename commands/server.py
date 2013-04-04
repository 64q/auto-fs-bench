#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import base.transmission


def test(host, port, modules):
    """Fonction permettant de vérifier que les modules sont valides sur le client"""
    
    return base.transmission.send_to_client(host, port, "test", params={"modules": modules})


def heartbeat(host, port):
    """Fonction permettant d'envoyer des msgs de type heartbeat"""
    
    return base.transmission.send_to_client(host, port, "heartbeat", timeout=0.1)


def run(host, port, test, conf):
    """Fonction permettant d'exécuter un test de benchmark"""
    
    return base.transmission.send_to_client(host, port, "run", params=conf)