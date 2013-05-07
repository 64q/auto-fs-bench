#encoding: utf-8

"""
Fichier permettant de manipuler le serveur auto-fs-bench

A appeller avec `python server.py [options]'

@author: Quentin
"""

import sys, os
import argparse, cmd
import csv

import core.utils, core.manager, core.tests
import core.commands.server
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
        # # paramétrage version fs
        # self.add_argument("-v", "--version", dest="version",
        #     help="parametrage de la version du fs")
        # port d'envoi du serveur aux clients
        self.add_argument("-p", "--port", default=config.server.send_port, type=int, dest="port", 
            help="port d'envoi du serveur (default: %i)" % config.server.send_port)


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
        """
        Fonction appellée par défaut si commande inconnue
        """

        print "error: unrecognized command '%s'." % line
    
    def do_run(self, test):
        """
        Fonction pour lancer un benchmark sur la plateforme
        """
        
        if test:
            try:
                # build de la configuration serveur
                server_config = core.manager.build_server_config(test, virtual=True)
                clients_results = dict()

                # affichage header kikoo
                core.utils.print_title("Benchmark '%s'" % test, ruler='=')

                print ">> Lancement des tests des clients"

                test_results = True

                # test des clients
                for client in server_config.clients:
                    test_response = core.commands.server.test(config.server.clients[client], config.server.send_port, server_config.modules)

                    if test_response["command"] == "error":
                        core.utils.print_row(client, test_response["returnValue"])
                        test_results = False

                if not test_results:
                    raise core.errors.TestsError("test() function failed on some clients")

                # cette fois les clients sont OK, on créé réellement le test
                server_config = core.manager.build_server_config(test)

                print ">> Debut du test module par module"

                for module in server_config.modules:
                    threads = list()
                    clients_results[module] = dict()

                    print ">> Execution du module '%s' en cours ..." % module

                    for client in server_config.clients:
                        # configuration du client à envoyer
                        client_config = core.manager.build_client_config(server_config, client, module)
                        client_ip_addr = config.server.clients[client]

                        # configuration et lancement du thread
                        thread = core.utils.threads_create_and_start(context, 
                            (clients_results[module], client, 
                                (client_ip_addr, config.server.send_port, client_config)))

                        # ajout dans la liste des threads
                        threads.append(thread)

                    # on attend que tous les threads se terminent pour continuer
                    sys.stdout.flush()
                    core.utils.threads_join_all(threads)

                    # enregistrement des résultats du module terminé
                    for client, result in clients_results[module].iteritems():
                        try:
                            # génération des chemins de sauvegarde
                            moduledir = core.manager.generate_moduledir(server_config, module)
                            filename = core.manager.generate_filename(server_config, module)

                            # on vérifie que le résultat n'est pas une erreur
                            core.transmission.check_transmission(result)

                            # sauvegarde des différents fichiers
                            core.tests.save_files(moduledir, filename, client, result)
                        except core.errors.ClientTransmissionError as e:
                            # enregistrement dans le fichier de résumé de l'erreur rencontrée
                            with open(filename, "ab") as csvfile:
                                core.utils.csv_write_line(csvfile, [client, e.__str__()])

                    sys.stdout.flush()

                print ">> Fin du test de benchmark"

                # lecture de chaque client et de ses résultats de thread
                for module, module_results in clients_results.iteritems():
                    core.utils.print_title("Resultats du module '%s'" % module)

                    core.utils.print_row("Client", "Etat", "Message"); print

                    for client, result in module_results.iteritems():
                        try:
                            # on vérifie que le résultat n'est pas une erreur
                            core.transmission.check_transmission(result)

                            # test passé avec succès, on affiche
                            core.utils.print_row(client, "PASSED")
                        except Exception as e:
                            # affichage de l'erreur dans la console
                            core.utils.print_row(client, "FAILED", e)
            # on capture toutes les exceptions qui pourraient être lancées pendant les traitements
            except Exception as e:
                print "error: %s" % e
        else:
            print "error: no test given"
            
    def help_run(self):
        print "\n".join(["- run <test>", "Lance un test de benchmark"])

    def do_test(self, test):
        """Fonction permettant de tester si un benchmark est lançable"""
        
        if test:
            try:
                server_config = core.manager.build_server_config(test, virtual=True)
                
                core.utils.print_title("Test de configuration du test '%s'" % test, ruler="=")

                core.utils.print_row("Client", "Etat", msg="Message"); print

                for client in server_config.clients:
                    # execution de la fonction de test sur chacun des client cible du test
                    response = core.commands.server.test(config.server.clients[client], config.server.send_port, server_config.modules)

                    if response["command"] == "test":
                        core.utils.print_row(client, "PASSED");
                    else:
                        core.utils.print_row(client, "FAILED", msg=response["returnValue"])
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
            core.utils.print_title("Liste des clients", ruler="=")

            core.utils.print_row("Client", "Etat", "Message"); print

            for client, ip in config.server.clients.iteritems():
                result = core.commands.server.heartbeat(ip, config.server.send_port)
                
                if result["command"] == "heartbeat":
                    core.utils.print_row(client, "Online")
                else:
                    core.utils.print_row(client, "Offline",result["returnValue"])
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
    result[client] = core.commands.server.run(params[0], params[1], params[2])

def main():
    """Fonction de main pour le serveur"""
    
    # parsage des arguments de la ligne de commande
    args = ServerArgumentParser().parse_args()

    # mise a jour du port d'envoi
    config.server.send_port = args.port
    
    print __description__

    # # ajout de la version du fs en override si présent
    # if not args.version is None:
    #     setattr(config.server, "fsversion", args.version)
    
    cmd = ServerCmd()

    # vérification de la présence du dossier de données et création
    if not os.path.exists(config.server.save_dir):
        try:
            os.mkdir(config.server.save_dir)
        except e:
            print "error: cannot create data dir"; return 1

    # lancement en mode interactif (Shell)
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