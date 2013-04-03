#encoding: utf-8

"""
Created on 26 févr. 2013

@author: Quentin
"""

import sys
import argparse, cmd

import conf
import commands.server

# definition des variables de description
__program__ = "auto-fs-bench"
__version__ = "0.1 (dev)"
__description__ = "auto-fs-bench executable"

class Server:
    """Classe contenant les configurations serveur"""
    
    clients = conf.load_config_app("clients")
    
    sport = 7979


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
    
    def do_load(self, line):
        if line:
            confs = conf.load_config_module(line)
            
            if confs:
                print "conf '%s' loaded successfully (param: %s)" % (line, confs["param"])
            else:
                print "error: no conf named '%s' found" % line
        else:
            print "error: no test given"
    
    def help_load(self):
        print "\n".join(["- load <file>", "Charge le fichier de configuration <file> pour ",
                         "faire les traitements necessaires"])
    
    def do_run(self, line):
        """Fonction pour lancer un benchmark sur la plateforme"""
        
        if line:
            confs = conf.load_config_module(line)
            
            for c in confs["clients"]:
                result = commands.server.run(Server.clients[c], Server.sport, line, confs)
                
                print "dist run '%s', result = %s" % (line, result["returnValue"])
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