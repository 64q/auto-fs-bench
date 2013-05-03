#encoding: utf-8

"""
Ce fichier contient des fonctions nécessaires pour transmettre et recevoir les infos par socket

@author: Quentin
"""

import sys
import socket, json, time

import core.errors
import core.commands.server


def send_to_client(host, port, call, params=None, timeout=1, blocking=1):
    """
    Fonction générique pour faire un appel distant
    """
    
    # requête envoyée au client
    request = {"command": call, "params": params}
    # réponse préfabriquée override si le client répond
    response = {"command": call, "params": params, "returnValue": None}
    # buffer nécessaire en socket non bloquantes
    buffer_recv = ""

    # Création de la socket en mode TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    done = 0

    time_spent = 0

    try:
        sock.connect((host, port))
        sock.sendall(json.dumps(request) + "\n")

        sock.setblocking(blocking)

        if blocking == 0:
            while done < 2:
                try:
                    current_recv = sock.recv(4096)
                    buffer_recv = buffer_recv + current_recv # FIXME

                    done = 1 # on commence à recevoir les données

                    if len(current_recv) == 0:
                        done = 2
                except socket.error:
                    # on ralenti légèrement la vitesse d'interrogation
                    time.sleep(1)
                    
                    # traitement du heartbeat toute les minutes
                    time_spent += 1

                    if time_spent == 60:
                        result = core.commands.server.heartbeat(host, port)

                        print "Envoi heartbeat ..."

                        if result["command"] != "heartbeat":
                            raise core.errors.ClientTimeoutError("client '%s' timeout" % host)

                        print "Heartbeat OK (%s)" % result["returnValue"]

                        time_spent = 0
        else:
            buffer_recv = sock.recv(4096) # FIXME
    except socket.timeout:
        raise core.errors.ClientTimeoutError("client '%s' timeout" % host)
    except socket.error as e:
        raise core.errors.ClientTimeoutError("client '%s' error: %s" % (host, e))
    finally:
        sock.close()

    try:
        response = json.loads(buffer_recv)
    except ValueError as e:
        raise core.errors.ClientTransmissionError("client '%s' transmission invalide" % host)

    return response

def retreive_response():
    """Récupère la réponse du client et jette une exception si il y a une erreur"""
    
def check_transmission(rq):
    """
    Vérifie que la transmission s'est bien passée, jette une exception s'il y a une erreur
    """
    if rq["command"] == "error":
        raise core.errors.ClientTransmissionError(rq["returnValue"])
    else:
        return True
            