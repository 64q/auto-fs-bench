#encoding: utf-8

"""
Fichier permettant de manipuler le client auto-fs-bench

A appeller avec `python server.py [options] server_addr'

@author: Quentin
"""

import sys
import json, argparse
import threading

import SocketServer

import config.client, commands.client

# configuration client
__program__ = "auto-fs-bench"
__version__ = "0.1 (dev)"
__description__ = "auto-fs-bench client executable"


class ClientArgumentParser(argparse.ArgumentParser):
    """Argument Parser pour le serveur"""
    
    def __init__(self):
        super(ClientArgumentParser, self).__init__()
        
        # initialisations
        self.description = "%s Version %s" % (__description__, __version__)
        
        # ajout des paramètres de lancement
        
        # lancement en mode deamon
        self.add_argument("-d", "--daemon", action="store_true", dest="daemon", 
                          help="lancement en demon")
        # lancement en mode verbeux
        self.add_argument("-v", "--verbose", action="count", dest="verbose", 
                          help="parametrage de la verbosite")
        # port d'écoute du client
        self.add_argument("-p", "--port", dest="port", default=config.client.listen_port, type=int, 
                          help="port d'ecoute du client (default: 7979)")


class ClientHandler(SocketServer.StreamRequestHandler):
    """Request handler for the TCP Client"""

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.rfile.readline().strip()
        
        request = json.loads(self.data)

        print "Receive from {0} request >> {1}".format(self.client_address[0], request)

        # traitement des commandes recues
        
        # heartbeat
        if request["command"] == "heartbeat":
            response = commands.client.heartbeat()
        # run
        elif request["command"] == "run":
            response = commands.client.run(request["params"])
        # test
        elif request["command"] == "test":
            response = commands.client.test(request["params"])
        # commande inconnue
        else:
            response = commands.client.error("Unknown command")
        
        print "Sent back response >> %s" % response
        
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """Classe necessaire pour threader le client"""


def main(argv=None):
    """Fonction de main pour le client"""
        
    args = ClientArgumentParser().parse_args()
    
    # config du port d'écoute
    config.client.listen_port = args.port
    
    print __description__
    print "[+] Lancement du client en écoute sur le port '%i'" % (config.client.listen_port)
    
    client = ThreadedTCPServer(("0.0.0.0", config.client.listen_port), ClientHandler)
    
    # lancement en mode demon (TODO)
    if args.daemon:
        client_thread = threading.Thread(target=client.serve_forever)
        client_thread.daemon = True
        client_thread.start()
    # lancement en mode normal
    else:
        client.serve_forever()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())