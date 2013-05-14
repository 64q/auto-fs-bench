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
__version__ = "0.9 (rendu)"
__description__ = "auto-fs-bench server executable"


class ServerArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser pour le serveur
    """
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__() # appel constructeur parent
        
        # initialisations
        self.description = "%s Version %s" % (__description__, __version__)
        
        # ajout des paramètres de lancement
        
        # test à lancer
        self.add_argument('bench_test', nargs="?", 
            help="test de benchmark a lancer (exemple: example), optionnel si -c est renseigne")
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
    """
    Shell pour auto-fs-bench
    """
    
    # message supplementaire CLI
    intro = "auto-fs-bench cmd utility. Entrez `help' pour plus d'informations"
    # apparence du prompt
    prompt = "srv: "
    # séparateur dans menus aide
    ruler = "-"
    
    def emptyline(self):
        pass
    
    def default(self, line):
        """
        Fonction appelée par défaut si commande inconnue

        Arguments:
        line -- la ligne de commande passée
        """

        print "error: commande '%s' non reconnue." % line
    
    def do_run(self, test):
        """
        Fonction pour lancer un benchmark sur la plateforme

        Arguments:
        test -- le test de benchmark à lancer
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
                        clients_results[client] = test_response["returnValue"]
                        test_results = False

                # si une erreur sur le test() des clients, on arrête le run
                if not test_results:
                    raise core.errors.TestsError()

                # cette fois les clients sont OK, on créé réellement le test
                server_config = core.manager.build_server_config(test)

                print ">> Debut du benchmark module par module"

                # lancement module par module des tests
                for module in server_config.modules:
                    threads = list()
                    clients_results[module] = dict()

                    print ">> Lancement du module '%s' ..." % module

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

                    # affichage des résultats du module
                    core.utils.print_title("Resultats du module '%s'" % module)
                    core.utils.print_row("Client", "Etat", "Message");

                    # enregistrement des résultats du module terminé
                    for client, result in clients_results[module].iteritems():
                        try:
                            # génération des chemins de sauvegarde
                            moduledir = core.manager.generate_moduledir(server_config, module)
                            filename = core.manager.generate_filename(server_config, module)

                            # on vérifie que le résultat n'est pas une erreur
                            core.transmission.check_transmission(result)

                            # test passé avec succès, on affiche
                            core.utils.print_row(client, "OK")

                            # sauvegarde des différents fichiers
                            core.tests.save_files(moduledir, filename, client, result)
                        except core.errors.ClientTransmissionError as e:
                            # affichage de l'erreur dans la console
                            core.utils.print_row(client, "KO", e)

                            # enregistrement dans le fichier de résumé de l'erreur rencontrée
                            with open(filename, "ab") as csvfile:
                                core.utils.csv_write_line(csvfile, [client, e.__str__()])

                    print ">> Fin d'exécution du module"; sys.stdout.flush()

                print ">> Fin du benchmark"
            # un client inconnu au bataillon ? On notifie !
            except core.errors.UnknownClientError as e:
                print "error: %s" % e
            # exception si test() a échoué sur clients
            except core.errors.TestsError as e:
                core.utils.print_title("Résumé des erreurs")
                core.utils.print_row("Client", "Etat", "Message")

                for client, error in clients_results.iteritems():
                    core.utils.print_row(client, "KO", error)
        else:
            print "error: aucun test renseigné"
            
    def help_run(self):
        print "\n".join(["- run <test>", "Lance un test de benchmark"])

    def do_test(self, test):
        """
        Fonction permettant de tester si un benchmark est lançable

        Arguments:
        test -- le test de benchmark à tester pour validité
        """
        
        if test:
            try:
                server_config = core.manager.build_server_config(test, virtual=True)
                
                core.utils.print_title("Test de configuration du benchmark '%s'" % test, ruler="=")
                core.utils.print_row("Client", "Etat", msg="Message");

                for client in server_config.clients:
                    # execution de la fonction de test sur chacun des client cible du test
                    response = core.commands.server.test(config.server.clients[client], 
                        config.server.send_port, server_config.modules)

                    if response["command"] == "test":
                        core.utils.print_row(client, "OK");
                    else:
                        core.utils.print_row(client, "KO", msg=response["returnValue"])
            except core.errors.UnknownClientError as e:
                print "error: %s" % e
            except ImportError as e:
                print "error: %s" % e
        else:
            print "error: aucun test renseigné"
    
    def help_test(self):
        print "\n".join(["- test <test>", "Lance un test de validité sur les \
            différents modules du test"])

    def do_list(self, line):
        """
        Listage des clients, envoie d'un heartbeat a partir de la liste

        Arguments:
        line -- le type de listing attendu (clients)
        """
        
        # listage des clients 
        if line == "clients":
            core.utils.print_title("Liste des clients", ruler="=")

            core.utils.print_row("Client", "Etat", "Message");

            for client, ip in config.server.clients.iteritems():
                result = core.commands.server.heartbeat(ip, config.server.send_port)
                
                if result["command"] == "heartbeat":
                    core.utils.print_row(client, "Online")
                else:
                    core.utils.print_row(client, "Offline", result["returnValue"])
        # type de listage inconnu
        else:
            print "error: le listage demandé n'est pas connu"
    
    def help_list(self):
        print "\n".join(["- list <clients>", "Affiche la liste des clients avec leur etat"])
    
    def do_save_dir(self, line):
        """
        Affiche le dossier de sauvegarde des données ou le change

        Arguments:
        line -- le dossier cible (optionnel)
        """

        if line:
            if not os.path.exists(line):
                try:
                    # tentative de création du dossier
                    os.mkdir(line)

                    # répertoire renseigné créé, on effectue le changement
                    config.server.save_dir = line
                except Exception as e:
                    print "error: impossible de créer le dossier de données (%s)" % e
            else:
                config.server.save_dir = line

        print "le répertoire de sauvegarde est '%s'" % config.server.save_dir
    
    def help_save_dir(self):
        print "\n".join(["- save_dir [path]", "Chemin de sauvegarde des tests"])

    def do_exit(self, line):
        print "sortie de auto-fs-bench"; sys.exit()
        
    def help_exit(self):
        print "\n".join(["- exit", "Quitte le shell du serveur"])
    
    def do_version(self, line):
        print "%s, v%s" % (__program__, __version__)
        
    def help_version(self):
        print "\n".join(["- version", "Affiche la version courante du serveur"])
    
    def help_help(self):
        print "\n".join(["- help <topic>", "Affiche l'aide sur <topic>"])


def context(result, client, params):
    """
    Fonction de contexte lancée dans un thread

    Arguments:
    result -- le dictionnaire des résultats modifié
    client -- le client qui va être cible du lancement
    params -- les paramètres de lancement de la fonction run
    """

    result[client] = core.commands.server.run(params[0], params[1], params[2])


def main():
    """
    Fonction de main pour le serveur
    """
    
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
            print "error: impossible de créer le dossier de données, sortie ..."; return 1

    # lancement en mode interactif (Shell)
    if args.shell:
        cmd.cmdloop()
    # lancement non interactif
    else:
        # renseignement du test à lancer
        if not args.bench_test is None:
            print ">> Lancement du benchmark '%s'" % args.bench_test

            cmd.onecmd('run ' + args.bench_test)
        else:
            print "error: aucun benchmark renseigné (à choisir dans la liste des \
                fichiers de 'config/tests/'"; return 1
            
    return 0

     
if __name__ == "__main__":
    sys.exit(main())