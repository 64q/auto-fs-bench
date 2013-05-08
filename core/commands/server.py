#encoding: utf-8

"""
Fichier contenant les commandes lançables par le serveur

@author: Quentin
"""

import core.transmission
import core.utils
import core.errors


def error(reason="Erreur generale"):
    """
    Fonction permettant de notifier une erreur au serveur en formattant un dictionnaire standard

    Arguments:
    reason -- raison de l'erreur déclenchée
    """

    response = dict(command = "error", returnValue = reason)

    return response


def test(host, port, modules=[]):
    """
    Fonction permettant de vérifier que le test est valide sur le client

    Arguments:
    host -- l'hôte cible du test
    port -- port d'envoi de la requête
    modules -- liste des modules à tester
    """
    
    response = dict()

    try:
        response = core.transmission.send_to_client(host, port, "test", params={"modules": modules})
    except core.errors.ClientTimeoutError as e:
        response = error(e.__str__())

    return response


def heartbeat(host, port, timeout=0.1):
    """
    Fonction permettant d'envoyer des msgs de type heartbeat

    Arguments:
    host -- l'hôte cible du test
    port -- port d'envoi de la requête
    timeout -- timeout toléré pour la réponse, évite un timeout sur un client chargé
    """

    response = dict()

    try:
        response = core.transmission.send_to_client(host, port, "heartbeat", timeout=timeout)
    except core.errors.ClientTimeoutError as e:
        response = error(e.__str__())

    return response


def run(host, port, conf=dict()):
    """
    Fonction permettant d'exécuter un test de benchmark, ici on pratique un send_to_client en mode
    non bloquant afin de récupérer de gros résultats (plus que 4096 caractères)

    host -- l'hôte cible du test
    port -- port d'envoi de la requête
    conf -- configuration de lancement du module
    """
    
    response = dict()

    try:
        response = core.transmission.send_to_client(host, port, "run", params=conf, blocking=0)
    except core.errors.ClientTimeoutError as e:
        response = error(e.__str__())

    return response