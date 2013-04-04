#encoding: utf-8

'''
Created on 4 avr. 2013

@author: Quentin
'''

import socket, json

def send_to_client(host, port, call, params=None, timeout=1):
    """Fonction générique pour faire un appel distant"""
    
    # requête envoyée au client
    request = {"command": call, "params": params}
    # réponse préfabriquée override si le client répond
    response = {"command": call, "params": params, "returnValue": False}

    # Création de la socket en mode TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        sock.connect((host, port))
        sock.sendall(json.dumps(request) + "\n")
    
        response = json.loads(sock.recv(1024))
    except:
        response = {"command": "error", "returnValue": "client '%s' timeout" % host}
    finally:
        sock.close()
        
    return response

def retreive_response():
    """Récupère la réponse du client et jette une exception si il y a une erreur"""
    
def check_transmission(rq):
    if rq["command"] == "error":
        return rq["returnValue"]
    else:
        return True
            