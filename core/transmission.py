#encoding: utf-8

'''
Created on 4 avr. 2013

@author: Quentin
'''

import sys
import socket, json, time

import core.errors


def send_to_client(host, port, call, params=None, timeout=1, blocking=1):
    """Fonction générique pour faire un appel distant"""
    
    # requête envoyée au client
    request = {"command": call, "params": params}
    # réponse préfabriquée override si le client répond
    response = {"command": call, "params": params, "returnValue": None}

    # Création de la socket en mode TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    done = False

    try:
        sock.connect((host, port))
        sock.sendall(json.dumps(request) + "\n")

        sock.setblocking(blocking)

        if blocking == 0:
            while not done:
                try:
                    response = json.loads(sock.recv(65536)) # FIXME
                    done = True # stop la boucle infinie, car données reçues
                except socket.error:
                    time.sleep(1)
        else:
            response = json.loads(sock.recv(65536)) # FIXME
    except socket.timeout:
        raise core.errors.ClientTimeoutError("client '%s' timeout" % host)
    finally:
        sock.close()
    
    return response

def retreive_response():
    """Récupère la réponse du client et jette une exception si il y a une erreur"""
    
def check_transmission(rq):
    if rq["command"] == "error":
        raise core.errors.ClientTransmissionError(rq["returnValue"])
    else:
        return True
            