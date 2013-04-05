#encoding: utf-8

'''
Created on 4 avr. 2013

@author: Quentin
'''

import socket, json, time

import core.errors


def send_to_client(host, port, call, params=None, timeout=1):
    """Fonction générique pour faire un appel distant"""
    
    # requête envoyée au client
    request = {"command": call, "params": params}
    # réponse préfabriquée override si le client répond
    response = {"command": call, "params": params, "returnValue": False}

    # Création de la socket en mode TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    done = False

    try:
        sock.connect((host, port))
        sock.sendall(json.dumps(request) + "\n")

        sock.setblocking(0)

        while not done:
            try:
                response = json.loads(sock.recv(1024))
                done = True
            except socket.error:
                print "no data received"
                time.sleep(1)
    except socket.timeout:
        raise core.errors.ClientTimeoutError("client '%s' timeout" % host)
    finally:
        sock.close()
        
    return response

def retreive_response():
    """Récupère la réponse du client et jette une exception si il y a une erreur"""
    
def check_transmission(rq):
    if rq["command"] == "error":
        raise ClientTransmissionError(rq["returnValue"])
    else:
        return True
            