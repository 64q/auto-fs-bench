#encoding: utf-8

"""
Fichier permettant de manipuler le serveur auto-fs-bench

A appeller avec `python server.py [options]'

@author: Quentin
"""

import sys, os
import argparse, cmd
import csv

import core.manager
import commands.server
import config.server

# definition des variables de description
__program__ = "auto-fs-bench"
__version__ = "0.1 (dev)"
__description__ = "auto-fs-bench executable"


class ServerArgumentParser(argparse.ArgumentParser):
    """Argument Parser pour le serveur"""
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__() # appel constructeur parent
        
        # initialisations
        self.description = "%s Version %s" % (__description__, __version__)
        
        # ajout des paramètres de lancement
        
        # test à lancer
        self.add_argument('bench_test', nargs="?",
                          help="test de benchmark a lancer, optionnel si -c est renseigne")
        # lancement en sous shell
        self.add_argument("-s", "--shell", action="store_true", dest="shell", 
                          help="lance la ligne de commande en mode interactif, ignore l'argument bench_test")
        # lancement en mode verbeux
        self.add_argument("-v", "--verbose", action="count", dest="verbose", 
                          help="parametrage du mode verbose")
        # fichier configuration du bench
        self.add_argument("-c", "--conf", default="app.cfg", dest="conf",
                          help="fichier config de l'application (default: app.cfg)")
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
            # build de la configuration serveur
            server_config = core.manager.build_server_config(test)
            clients_results = dict()
            threads = list()
            
            for client in server_config.clients:
                # configuration du client à envoyer
                client_config = core.manager.build_client_config(server_config, client)
                client_ip_addr = config.server.clients[client]

                # configuration et lancement du thread
                thread = core.utils.threads_create_and_start(context, (clients_results, client, (client_ip_addr, config.server.send_port, client_config)))

                # ajout dans la liste des threads
                threads.append(thread)
                
            core.utils.threads_join_all(threads)
            
            # lecture des résultats obtenus et stockage
            for module in server_config.modules:
                # ouverture du fichier en écriture
                moduledir = core.manager.generate_moduledir(server_config, module)
                filename = core.manager.generate_filename(server_config, module)
                # ouverture en mode append du fichier
                csvfile = open(filename, "ab")
                csvwriter = csv.writer(csvfile)
                
                # écriture des résultats de chacun des clients
                for client, result in clients_results.iteritems():

                    print ">> client '%s' returns '%s'" % (client, result)

                    try:
                        core.transmission.check_transmission(result)

                        for thid, thout in result["returnValue"][module].iteritems():
                            csvwriter.writerow([client + "_" + thid, thout["return"]])

                            # création des fichiers de sortie du module de benchmark
                            for fn, ct in thout["files"].iteritems():
                                fp = open(moduledir + "/" + fn, "w")
                                fp.write(ct)
                                fp.close()

                    except core.errors.ClientTransmissionError as e:
                        csvwriter.writerow([client, e.strerror])
                    
                csvfile.close()

        else:
            print "error: no test given"
            
    def help_run(self):
        print "\n".join(["- run <test>", "Lance un test de benchmark"])

    def do_test(self, test):
        """Fonction permettant de tester si un benchmark est lançable"""
        
        if test:
            print "Test de configuration du test '%s'" % test

            for client, ip in config.server.clients.iteritems():
                result = commands.server.test(ip, config.server.send_port, test)
                
                if result:
                    print "%s: %s" % (client, "Operationnel")
                else:
                    print "%s: %s" % (client, "En erreur")
        else:
            print "error: no test given"
    
    def help_test(self):
        print "\n".join(["- test <test>", "Lance un test de validite sur les differents modules du test"])

    def do_list(self, line):
        """Listage des clients, envoie d'un heartbeat a partir de la liste"""
        
        # listage des clients 
        if line == "clients":
            print "Test de heartbeat des clients"

            for client, ip in config.server.clients.iteritems():
                result = commands.server.heartbeat(ip, config.server.send_port)
                
                if result:
                    print "  %s: %s" % (client, "Online")
                else:
                    print "  %s: %s" % (client, "Offline")

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
    
    # limitation verbosity a 3
    if args.verbose:
        if args.verbose > 3:
            args.verbose = 3
        
        print "[+] Lancement en mode verbeux (niveau: %i)" % args.verbose
    
    # lancement en mode interactif (CLI)
    if args.shell:
        ServerCmd().cmdloop()
    # lancement non interactif
    else:
        # renseignement du test à lancer
        if not args.bench_test is None:
            print "[+] Lancement du test de benchmark '%s'" % args.bench_test
        else:
            print "error: no benchmark test given"; return 1
            
    return 0

     
if __name__ == "__main__":
    sys.exit(main())