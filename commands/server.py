#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import socket, json

def heartbeat(addr):
    """Fonction permettant d'envoyer des msgs de type heartbeat"""
    
    state = False
    data = json.dumps({"command": "heartbeat"})

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # modification du timeout pour le heartbeat
    sock.settimeout(0.1)
    
    try:
        # Connect to server and send data
        sock.connect((addr, 7979))
        sock.sendall(data + "\n")
    
        # Receive data from the server and shut down
        received = sock.recv(1024)
        
        # receive response
        response = json.loads(received)
    
        if "ok" == response["result"]:
            state = True
    except:
        pass
    finally:
        sock.close()
        
    return state