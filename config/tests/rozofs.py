#encoding: utf-8

"""
Ce fichier est un exemple de fichier de configuration d'un test de benchmark

Pour l'utiliser, il suffit de le lancer via la commande `run' du shell afs

@author Quentin
"""

# configuration du test de benchmark

# nom du test de benchmark (doit être identique au nom du fichier)
name = "rozofs"

# commentaire éventuel sur le test
comment = "test du systeme rozofs"

# modules de test à lancer
modules = ["pjdtest", "cp", "dd", "fdtree", "fileop", "iozone", "rsync"]

# liste des clients cibles du test
clients = {
    "rozo3": {"path": "/mnt/rozofs@1.1.100.15/demo", "times": 1}
}

# spécifications sur le système de fichier testé
fs = {
    "name": "rozofs",
    "version": "1.7"
}

# fin de configuration du test