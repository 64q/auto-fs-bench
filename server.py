#encoding: utf-8

"""
Created on 26 févr. 2013

@author: Quentin
"""

import sys
import argparse, cmd

import conf

# definition de quelques variables internes au serveur
__program__ = "auto-fs-bench"
__version__ = "0.1 (dev)"
__description__ = "Ligne de commande serveur pour auto-fs-bench."

class ServerArgumentParser(argparse.ArgumentParser):
    """Argument Parser pour le serveur"""
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__()
        
        # initialisations
        self.description = "%s Version %s" % (__description__, __version__)
        
        # ajout des paramètres de lancement
        self.add_argument('bench_file', nargs="?", help="fichier de benchmark a executer, optionnel si -c est renseigne")
        self.add_argument("-c", "--cli", action="store_true", dest="cli", help="lance la ligne de commande en mode interactif, ignore l'argument bench_file")
        self.add_argument("-v", "--verbose", action="count", dest="verbose", help="parametrage de la verbosite")


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
            confs = conf.load(line)
            # affichage après chargement
            print "conf '%s' loaded successfully" % confs["name"]
    
    def do_exit(self, line):
        print "exiting auto-fs-bench"; sys.exit() 
        
    def help_exit(self):
        print "\n".join(["exit", "Quitte la CLI du serveur"])
    
    def do_version(self, line):
        print "%s, v%s" % (__program__, __version__)
        
    def help_version(self):
        print "\n".join(["version", "Affiche la version courante du serveur"])
    
    def do_EOF(self, line):
        return True


def main():
    """Fonction de main pour le serveur"""
    
    args = ServerArgumentParser().parse_args()
    
    print __description__
    
    if args.verbose:
        # limitation verbosity a 3
        if args.verbose > 3:
            args.verbose = 3
        
        print "[+] Lancement en mode verbeux (niveau: %i)" % args.verbose
    
    if args.cli:
        ServerCmd().cmdloop()
    else:
        if not args.bench_file is None:
            print "[+] Lecture du fichier de benchmark '%s'" % args.bench_file
        else:
            print "error: missing file bench config"; return 1
            
    return 0
        
if __name__ == "__main__":
    sys.exit(main())