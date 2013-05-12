#encoding: utf-8

"""
Fichier permettant de manipuler le client auto-fs-bench

A appeller avec `python server.py [options]'

@author: Quentin
"""

import sys
import json
import argparse
import threading

import SocketServer

import config.client
import core.commands.client

# configuration client
__program__ = "auto-fs-bench"
__version__ = "0.9 (rendu)"
__description__ = "auto-fs-bench client executable"


class ClientArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser pour le serveur
    """
    
    def __init__(self):
        super(ClientArgumentParser, self).__init__()
        
        # initialisations
        self.description = "%s, Version %s" % (__description__, __version__)
        
        # ajout des paramètres de lancement
        
        # lancement en mode deamon
        self.add_argument("-d", "--daemon", action="store_true", dest="daemon", 
            help="lancement en demon")
        # port d'écoute du client
        self.add_argument("-p", "--port", dest="port", default=config.client.listen_port, type=int, 
            help="port d'ecoute du client (default: 7979)")


class ClientHandler(SocketServer.StreamRequestHandler):
    """
    Request handler pour le client TCP
    """

    def handle(self):
        self.data = self.rfile.readline().strip()

        try:
            # chargement de la chaine JSON reçue, on la met dans le bloc try..catch afin de 
            # prévenir des erreurs lors du décodage
            request = json.loads(self.data)

            print ">> Receive from {0} request >> {1}".format(self.client_address[0], request)

            # traitement des commandes recues en appelant directement la commande du module
            # munie des bons paramètres de lancement
            response = getattr(core.commands.client, request["command"])(request["params"])
        except Exception as e:
            response = core.commands.client.error("%s" % e)

        # print ">> Sent back response >> %s" % response
        
        self.request.sendall(json.dumps(response))


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    Classe necessaire pour threader le client
    """

    pass


def main():
    """
    Fonction de main pour le client
    """
    
    # parsage des arguments    
    args = ClientArgumentParser().parse_args()
    
    # config du port d'écoute
    config.client.listen_port = args.port
    
    print __description__
    print ">> Lancement du client en écoute sur le port '%i'" % (config.client.listen_port)
    print ">> Appuyez sur Ctrl+C pour fermer le client"
    
    client_server = ThreadedTCPServer(("0.0.0.0", config.client.listen_port), ClientHandler)
    
    # lancement en mode demon (TODO)
    if args.daemon:
        client_thread = threading.Thread(target=client.serve_forever)
        client_thread.daemon = True
        client_thread.start()
    # lancement en mode normal
    else:
        client_server.serve_forever()

    return 0


if __name__ == '__main__':
    sys.exit(main())