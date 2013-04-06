#encoding: utf-8

"""
Fichier permettant de manipuler le serveur auto-fs-bench

A appeller avec `python server.py [options]'

@author: Quentin
"""

import sys, os
import argparse, cmd
import csv

import core.manager, core.tests
import commands.server
import config.server

# definition des variables de description
__program__ = "auto-fs-bench"
__version__ = "0.1 (dev)"
__description__ = "auto-fs-bench server executable"


class ServerArgumentParser(argparse.ArgumentParser):
    """Argument Parser pour le serveur"""
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__() # appel constructeur parent
        
        # initialisations
        self.description = "%s Version %s" % (__description__, __version__)
        
        # ajout des paramètres de lancement
        
        # test à lancer
        self.add_argument('bench_test', nargs="?",
                          help="test de benchmark a lancer (exemple: simple), optionnel si -c est renseigne")
        # lancement en sous shell
        self.add_argument("-s", "--shell", action="store_true", dest="shell",
                          help="lance la ligne de commande en mode interactif, ignore l'argument bench_test")
        # lancement en mode verbeux
        self.add_argument("-v", "--verbose", action="count", dest="verbose", 
                          help="parametrage du mode verbose")
        # port d'envoi du serveur aux clients
        self.add_argument("-p", "--port", default=config.server.send_port, type=int, dest="port", 
                          help="port d'envoi du serveur (default: 7979)")


class ServerCmd(cmd.Cmd):
    """Shell pour auto-fs-bench."""
    
    # message supplementaire CLI
    intro = "auto-fs-bench cmd utility. Type `help' for more information"
    # apparence du prompt
    prompt = "srv: "
    # séparateur dans menus aide
    ruler = "-"
    
    def emptyline(self):
        pass
    
    def default(self, line):
        print "error: unrecognized command '%s'." % line
    
    def do_run(self, test):
        """Fonction pour lancer un benchmark sur la plateforme"""
        
        if test:
            print "Test de benchmark '%s'" % test

            try:
                # build de la configuration serveur
                server_config = core.manager.build_server_config(test)
                clients_results = dict()
                threads = list()
                
                for client in server_config.clients:
                    # configuration du client à envoyer
                    client_config = core.manager.build_client_config(server_config, client)
                    client_ip_addr = config.server.clients[client]

                    # configuration et lancement du thread
                    thread = core.utils.threads_create_and_start(context, 
                        (clients_results, client, (client_ip_addr, config.server.send_port, client_config)))

                    # ajout dans la liste des threads
                    threads.append(thread)
                
                # on attend que tous les threads se terminent pour continuer    
                core.utils.threads_join_all(threads)
                
                # lecture de chaque client et de ses résultats de thread
                for client, result in clients_results.iteritems():
                    try:
                        # on vérifie que le résultat n'est pas une erreur
                        core.transmission.check_transmission(result)

                        print "  %s\t: resultat du test OK" % client

                        # on boucle sur tous les threads du client récupéré
                        for modname, threads_results in result["returnValue"].iteritems():
                            # génération des chemins de sauvegarde
                            moduledir = core.manager.generate_moduledir(server_config, modname)
                            filename = core.manager.generate_filename(server_config, modname)

                            # sauvegarde des différents ichiers
                            core.tests.save_files(moduledir, filename, client, threads_results)
                    except Exception as e:
                        print "  %s\t: erreur de transmission (error: %s)" % (client, e)
            except ImportError as e:
                print "error: %s" % e
        else:
            print "error: no test given"
            
    def help_run(self):
        print "\n".join(["- run <test>", "Lance un test de benchmark"])

    def do_test(self, test):
        """Fonction permettant de tester si un benchmark est lançable"""
        
        if test:
            print "Test de configuration du test '%s'" % test

            server_config = core.manager.build_server_config(test)

            try:
                for client in server_config.clients:
                    # execution de la fonction de test sur chacun des client cible du test
                    response = commands.server.test(config.server.clients[client], config.server.send_port, server_config.modules)

                    if response["command"] == "test":
                        print "  %s\t: %s" % (client, "test operationnel")
                    else:
                        print "  %s\t: %s" % (client, "erreur lors du test (error: %s)" % response["returnValue"])
            except ImportError as e:
                print "error: %s" % e
        else:
            print "error: no test given"
    
    def help_test(self):
        print "\n".join(["- test <test>", "Lance un test de validite sur les differents modules du test"])

    def do_list(self, line):
        """Listage des clients, envoie d'un heartbeat a partir de la liste"""
        
        # listage des clients 
        if line == "clients":
            print "Liste des clients"

            for client, ip in config.server.clients.iteritems():
                result = commands.server.heartbeat(ip, config.server.send_port)
                
                if result["command"] == "heartbeat":
                    print "  %s\t: %s" % (client, "Online")
                else:
                    print "  %s\t: %s" % (client, "Offline (error: %s)" % result["returnValue"])
        # listage des tests disponibles
        elif line == "tests":
            print "Liste des tests de benchmark"
        # type de listage inconnu
        else:
            print "error: unrecognized type of listing"
    
    def help_list(self):
        print "\n".join(["- list <clients>", "Affiche la liste des clients avec leur etat"])
    
    def do_save_dir(self, line):
        if line:
            if os.path.isdir(line):
                config.server.save_dir = line
            else:
                print "error: invalid dir '%s'" % line
        else:
            print "current dir is '%s'" % config.server.save_dir
    
    def help_save_dir(self):
        print "\n".join(["- save_dir [path]", "Chemin de sauvegarde des tests"])

    def do_exit(self, line):
        print "exiting auto-fs-bench"; sys.exit()
        
    def help_exit(self):
        print "\n".join(["- exit", "Quitte la CLI du serveur"])
    
    def do_version(self, line):
        print "%s, v%s" % (__program__, __version__)
        
    def help_version(self):
        print "\n".join(["- version", "Affiche la version courante du serveur"])
    
    def help_help(self):
        print "\n".join(["- help <topic>", "Affiche l'aide sur <topic>"])


def context(result, client, params):
    result[client] = commands.server.run(params[0], params[1], params[2])

def main():
    """Fonction de main pour le serveur"""
    
    # parsage des arguments de la ligne de commande
    args = ServerArgumentParser().parse_args()

    # mise a jour du port d'envoi
    config.server.send_port = args.port
    
    print __description__

    # limitation verbosity a 3
    if args.verbose:
        if args.verbose > 3:
            args.verbose = 3
        
        print ">> Lancement en mode verbeux (niveau: %i)" % args.verbose
    
    cmd = ServerCmd()

    

    # lancement en mode interactif (CLI)
    if args.shell:
        cmd.cmdloop()
    # lancement non interactif
    else:
        # renseignement du test à lancer
        if not args.bench_test is None:
            print ">> Lancement du test de benchmark '%s'" % args.bench_test

            cmd.onecmd('run ' + args.bench_test)
        else:
            print "error: no benchmark test given"; return 1
            
    return 0

     
if __name__ == "__main__":
    sys.exit(main())