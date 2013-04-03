#encoding: utf-8

"""
Created on 26 févr. 2013

@author: Quentin
"""

import sys
import argparse, cmd

import conf
import commands.server

# definition de quelques variables internes au serveur
__program__ = "auto-fs-bench"
__version__ = "0.1 (dev)"
__description__ = "Executable serveur pour auto-fs-bench."


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
        self.add_argument('bench_file', nargs="?", 
                          help="fichier de benchmark a executer, optionnel si -c est renseigne")
        self.add_argument("-c", "--cli", action="store_true", dest="cli", 
                          help="lance la ligne de commande en mode interactif, ignore l'argument bench_file")
        self.add_argument("-v", "--verbose", action="count", dest="verbose", 
                          help="parametrage de la verbosite")
        self.add_argument('--sport', default=7979, type=int, 
                          help="port d'envoi du serveur (default: 7979)")


class ServerCmd(cmd.Cmd):
    """CLI pour auto-fs-bench."""
    
    # message supplementaire CLI
    intro = "CLI utility, type \"help\" for more information"
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
        """EOF"""
        
        return True
    
    def help_help(self):
        print "\n".join(["- help <topic>", "Affiche l'aide sur <topic>"])
    
def main():
    """Fonction de main pour le serveur"""
    
    # parsage des arguments de la ligne de commande
    args = ServerArgumentParser().parse_args()
    
    print __description__
    
    # limitation verbosity a 3
    if args.verbose:
        if args.verbose > 3:
            args.verbose = 3
        
        print "[+] Lancement en mode verbeux (niveau: %i)" % args.verbose
    
    # lancement en mode interactif (CLI)
    if args.cli:
        ServerCmd().cmdloop()
    # lancement non interactif
    else:
        # presence du fichier de config bench
        if not args.bench_file is None:
            print "[+] Lecture du fichier de benchmark '%s'" % args.bench_file
        else:
            print "error: missing file bench config"; return 1
            
    return 0
        
if __name__ == "__main__":
    sys.exit(main())