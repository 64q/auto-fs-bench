#encoding: utf-8

"""
Ce fichier est un exemple de fichier de configuration d'un test de benchmark

Pour l'utiliser, il suffit de le lancer via la commande `run' du shell afs

@author Quentin
"""

# configuration du test de benchmark

# nom du test de benchmark (doit être identique au nom du fichier)
name = "c07"

# commentaire éventuel sur le test
comment = "bash scripts test"

# modules de test à lancer
modules = ["bonnie", "cp", "dd", "fdtree", "fileop", "iozone", "rsync"]

# liste des clients cibles du test
clients = {
    "ptrans1": {"path": "/srv", "times": 1},
    "ptrans2": {"path": "/srv", "times": 1},
    "ptrans3": {"path": "/srv", "times": 1}
}

# spécifications sur le système de fichier testé
fs = {
    "name": "rozofs",
    "version": "0.1"
}

# fin de configuration du test