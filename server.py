# encoding: utf-8

"""
Created on 26 févr. 2013

@author: Quentin
"""

import sys
import argparse
import cmd

__program__ = "auto-fs-bench"
__version__ = "0.1"
__description__ = "Ligne de commande serveur pour auto-fs-bench."

class ServerArgumentParser(argparse.ArgumentParser):
    """Argument Parser pour le serveur"""
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__()
        
        # initialisations
        self.description = __description__
        
        # ajout des paramètres de lancement
        self.add_argument('bench_file', nargs="?", help="fichier de benchmark a executer")
        self.add_argument("-c", "--cli", action="store_true", dest="cli", help="lance la ligne de commande en mode interactif")
        self.add_argument("-v", "--verbose", action="count", dest="verbose", help="parametrage de la verbosite")


class ServerCmd(cmd.Cmd):
    """CLI pour auto-fs-bench."""
    
    prompt = "srv: "
    ruler = "-"
    
    def do_exit(self, line):
        sys.exit()
        
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
        print "[+] Lecture du fichier de benchmark '%s'" % args.bench_file

        
if __name__ == "__main__":
    sys.exit(main())