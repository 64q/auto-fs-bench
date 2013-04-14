#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import json
import sys
import time

import core.errors
import core.monitoring
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
    
    response = dict(command = "test", returnValue = None)

    try:
        print "params", params
        # chargement du module en mémoire
        mods = bench.modLoad([params["module"]])

        # Monitoring de la machine pendant les tests
        monitor = core.monitoring.Monitoring()
        monitor.start()
        print "aaaaaaaaaaa"
        time.sleep(5)   # Tempo de 5 secondes pour avoir l'état de base de la machine
        print "bbbbbbbb"

        # exécution de la fonction de run du module
        response["returnValue"] = bench.modLaunch(mods[params["module"]], "run", params["path"], nb=params["times"])
        print "cccccccccc"
        
        # Arret du monitoring et récupération des données
        response["monitoring"] = dict()
        response["monitoring"] = core.monitoring.graphFile(monitor.stop())
        # print core.monitoring.graphFile(monitor.stop())

        print "return", response["returnValue"]
    except core.errors.InvalidModuleError as e:
        response = error(e.__str__())
        monitor.stop()  # Arret du thread de monitoring
    except:
        print "Unexpected error:", sys.exc_info()[0]
        monitor.stop()  # Arret du thread de monitoring
        raise

    return response
