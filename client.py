#encoding: utf-8

'''
Created on 27 févr. 2013

@author: Quentin
'''

import sys
import json, argparse
import threading

import SocketServer

import commands.client

# configuration client
__program__ = "auto-fs-bench"
__version__ = "0.1 (dev)"
__description__ = "Executable client pour auto-fs-bench."

# config du client (tcpserver)
__lport__ = 7979


class ClientArgumentParser(argparse.ArgumentParser):
    """Argument Parser pour le serveur"""
    
    def __init__(self):
        super(ClientArgumentParser, self).__init__()
        
        # initialisations
        self.description = "%s Version %s" % (__description__, __version__)
        
        # ajout des paramètres de lancement
        
        # adresse du serveur de benchmark
        self.add_argument('server_addr', 
                          help="adresse du serveur de benchmark")
        # lancement en mode deamon
        self.add_argument("-d", "--daemon", action="store_true", dest="daemon", 
                          help="lancement en demon")
        # lancement en mode verbeux
        self.add_argument("-v", "--verbose", action="count", dest="verbose", 
                          help="parametrage de la verbosite")
        # port d'écoute du client
        self.add_argument('--lport', default=7979, type=int, 
                          help="port d'ecoute du client (default: 7979)")


class ClientHandler(SocketServer.StreamRequestHandler):
    """Request handler for the TCP Client"""

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.rfile.readline().strip()
        
        print "receive from {}".format(self.client_address[0])
        
        request = json.loads(self.data)
        
        print ">>>>", request
        
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
            response = commands.client.error()
        
        print ">> sent back: %s" % response
        
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """Classe necessaire pour threader le client"""


def main(argv=None):
    """Fonction de main pour le client"""
        
    args = ClientArgumentParser().parse_args()
    
    # config srv
    __lport__ = args.lport
    
    print __description__
    print "[+] Lancement du client en connexion sur serveur %s:%i" % (args.server_addr, __lport__)
    
    client = ThreadedTCPServer(("127.0.0.1", __lport__), ClientHandler)
    
    # lancement en mode demon
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