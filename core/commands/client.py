#encoding: utf-8

"""
Fichier contenant les commandes lançables par le client

@author: Quentin
"""

import json
import sys
import time

import core.errors
import core.monitoring
import core.benchutils


def error(reason="Erreur generale"):
    """
    Fonction permettant de notifier une erreur au serveur en formattant un dictionnaire standard

    Arguments:
    reason -- raison de l'erreur déclenchée
    """
    
    response = dict(command = "error", returnValue = reason)

    return response


def test(params):
    """
    Fonction permettant de tester si le client est correctement initialisé

    Arguments:
    params -- dictionnaire de paramètres contenant notamment les modules à tester
    """
    
    response = dict(command = "test", returnValue = True)

    try:
        # chargement des modules nécessaires au test
        modules = core.benchutils.modLoad(params["modules"])

        # test de chacun des modules
        for modname, modfns in modules.iteritems():
            modfns.test()
    except core.errors.InvalidModuleError as e:
        response = error(e.__str__())

    return response


def heartbeat(params=None):
    """
    Réponse à un heartbeat

    Arguments:
    params -- dictionnaire de paramètres (inutilisés ici)
    """
    
    response = dict(command = "heartbeat", returnValue = True)

    return response


def run(params):
    """
    Fonction pour effectuer un test de benchmark

    Arguments:
    params -- dictionnaire des paramètres contenant le module à exectuer et le nombre de thread
    """
    
    response = dict(command = "test", returnValue = None)

    try:
        # print ">> params = %s" % params
        # chargement du module en mémoire
        mods = core.benchutils.modLoad([params["module"]])

        # Monitoring de la machine pendant les tests
        monitor = core.monitoring.Monitoring()
        monitor.start()
        time.sleep(5) # Tempo de 5 secondes pour avoir l'état de base de la machine

        # exécution de la fonction de run du module
        response["returnValue"] = core.benchutils.modLaunch(mods[params["module"]], 
            "run", params["path"], nb=params["times"])
        
        # Arret du monitoring et récupération des données
        response["monitoring"] = dict()
        response["monitoring"] = core.monitoring.graphFile(monitor.stop())

        # print ">> return = %s" % response["returnValue"]
    except core.errors.InvalidModuleError as e:
        response = error(e.__str__())
    except Exception as e:
        print "error: %s (sysinfo: %s)" % (e, sys.exc_info()[0])
        monitor.stop()  # Arret du thread de monitoring
        response = error(e.__str__())

    return response
