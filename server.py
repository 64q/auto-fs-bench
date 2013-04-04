#encoding: utf-8

"""
Created on 26 févr. 2013

@author: Quentin
"""

import sys, os
import argparse, cmd

import csv, shutil, threading

import base.conf, base.manager
import commands.server

# definition des variables de description
__program__ = "auto-fs-bench"
__version__ = "0.1 (dev)"
__description__ = "auto-fs-bench executable"


class Server:
    """Classe contenant les configurations serveur"""
    
    clients = base.conf.load_config_app("clients")
    
    sport = 7979
    
    save_dir = "data/"


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
                          help="parametrage de la verbosite")
        # fichier configuration du bench
        self.add_argument("-c", "--conf", default="app.cfg", dest="conf",
                          help="fichier config de l'application (default: app.cfg)")
        # port d'envoi du serveur aux clients
        self.add_argument("-p", "--port", default=7979, type=int, dest="port", 
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
    
    #===========================================================================
    # def do_load(self, line):
    #    if line:
    #        confs = conf.load_config_module(line)
    #        
    #        if confs:
    #            print "conf '%s' loaded successfully (param: %s)" % (line, confs["param"])
    #        else:
    #            print "error: no conf named '%s' found" % line
    #    else:
    #        print "error: no test given"
    # 
    # def help_load(self):
    #    print "\n".join(["- load <file>", "Charge le fichier de configuration <file> pour ",
    #                     "faire les traitements necessaires"])
    #===========================================================================
    
    def do_run(self, line):
        """Fonction pour lancer un benchmark sur la plateforme"""
        
        if line:
            sv_config = base.manager.build_sv_config(line)
            cl_results = dict()
            threads = dict()
            
            # lancement des tests en parallèle (TODO)
            for client, client_conf in sv_config["clients"].iteritems():
                # configuration du client à envoyer
                cl_config = base.manager.build_cl_config(sv_config, client_conf)
                threads[client] = threading.Thread(None, context, None, (cl_results, client, (Server.clients[client], Server.sport, line, cl_config)))
                
                threads[client].start()
                
            for client in sv_config["clients"]:
                threads[client].join()
            
            # lecture des résultats obtenus et stockage
            for module in sv_config["modules"]:
                # ouverture du fichier en écriture
                csvfile = open(base.manager.filepath(sv_config, module), "ab")
                csvwriter = csv.writer(csvfile)
                
                # écriture des résultat de chacun des clients
                for client, client_conf in sv_config["clients"].iteritems():
                    checking = base.transmission.check_transmission(cl_results[client])
                    
                    if True == checking:
                        csvwriter.writerow([client, cl_results[client]["returnValue"][module]])
                    else:
                        print checking
                    
                csvfile.close()
            
            # copie de la configuration du test dans le dossier de sauvegarde
            shutil.copyfile("conf/" + line + ".cfg", sv_config["dirpath"] + "/" + line + ".cfg")
        else:
            print "error: no test given"
            
    
    def do_test(self, line):
        """Fonction permettant de tester si un benchmark est lançable"""
        
        if line:
            for c in Server.clients:
                result = commands.server.test(Server.clients[c], Server.sport, line.split())
                
                print "%s: %r" % (c, result)
        else:
            print "error: no test given"
    
    def do_list(self, line):
        """Listage des clients, envoie d'un heartbeat a partir de la liste"""
        
        # listage des clients 
        if line == "clients":
            for k, v in Server.clients.items():
                result = commands.server.heartbeat(v, Server.sport)
                
                print " %s: %r" % (k, result["returnValue"])
        # type de listage inconnu
        else:
            print "error: unrecognized type of listing"
    
    def help_list(self):
        print "\n".join(["- list clients", "Affiche la liste des clients avec etat"])
    
    def do_save_dir(self, line):
        if line:
            if os.path.isdir(line):
                Server.save_dir = line
            else:
                print "error: invalid dir '%s'" % line
        else:
            print "current dir is '%s'" % Server.save_dir
    
    def do_exit(self, line):
        print "exiting auto-fs-bench"; sys.exit()
        
    def help_exit(self):
        print "\n".join(["- exit", "Quitte la CLI du serveur"])
    
    def do_version(self, line):
        print "%s, v%s" % (__program__, __version__)
        
    def help_version(self):
        print "\n".join(["- version", "Affiche la version courante du serveur"])
    
    def do_EOF(self, line):
        return True
    
    def help_help(self):
        print "\n".join(["- help <topic>", "Affiche l'aide sur <topic>"])


def context(result, client, params=()):
    result[client] = commands.server.run(params[0], params[1], params[2], params[3])

def main():
    """Fonction de main pour le serveur"""
    
    # parsage des arguments de la ligne de commande
    args = ServerArgumentParser().parse_args()
    
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