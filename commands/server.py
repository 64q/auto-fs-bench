#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import socket, json

def dist_call(host, port, call, params=None, timeout=1):
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
        pass
    finally:
        sock.close()
        
    return response

def heartbeat(host, port):
    """Fonction permettant d'envoyer des msgs de type heartbeat"""
    
    return dist_call(host, port, "heartbeat", timeout=0.1)

def run(host, port, test, conf):
    """Fonction permettant d'exécuter un test de benchmark"""
    
    return dist_call(host, port, "run", params={"test": test, "conf": conf})