#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import json

import core.errors
import bench


def error(reason="Generic error"):
    """Fonction permettant de notifier une erreur au serveur"""
    
    response = dict(command = "error", returnValue = reason)

    return response


def test(params):
    """ Fonction permettant de tester si le client est correctement initialisé"""
    
    response = dict(command = "test", returnValue = True)

    try:
        # chargement des modules nécessaires au test
        modules = bench.modLoad(params["modules"])

        # test de chacun des modules
        for modname, modfns in modules.iteritems():
            modfns.test()
    except core.errors.InvalidModuleError as e:
        response = error(e.__str__())

    return response


def heartbeat(params=None):
    """Réponse à un heartbeat"""
    
    response = dict(command = "heartbeat", returnValue = True)

    return response


def run(params):
    """Fonction pour effectuer un test de benchmark"""
    
    results = dict()
    response = dict(command = "test", returnValue = None)

    try:
        mods = bench.modLoad(params["modules"])

        for k in params["modules"]:
            module = mods[k]

            results[k] = bench.modLaunch(module, "run", params["path"], nb=params["times"])

        response["returnValue"] = results
    except core.errors.InvalidModuleError as e:
        response = error(e.__str__())

    return response
