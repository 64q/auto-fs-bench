#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import core.transmission, core.utils, core.errors


def __error__(reason="Generic Reason"):
    """
    Fonction pour renvoyer une erreur
    """

    response = dict(command = "error", returnValue = reason)

    return response


def test(host, port, modules=[]):
    """Fonction permettant de vérifier que le test est valide sur le client"""
    
    response = dict()

    try:
        response = core.transmission.send_to_client(host, port, "test", params={"modules": modules})
    except core.errors.ClientTimeoutError as e:
        response = __error__(e.__str__())

    return response


def heartbeat(host, port):
    """Fonction permettant d'envoyer des msgs de type heartbeat"""

    response = dict()

    try:
        response = core.transmission.send_to_client(host, port, "heartbeat", timeout=0.1)
    except core.errors.ClientTimeoutError as e:
        response = __error__(e.__str__())

    return response


def run(host, port, conf=dict()):
    """Fonction permettant d'exécuter un test de benchmark"""
    
    response = dict()

    try:
        response = core.transmission.send_to_client(host, port, "run", params=conf, blocking=0)
    except core.errors.ClientTimeoutError as e:
        response = __error__(e.__str__())

    return response