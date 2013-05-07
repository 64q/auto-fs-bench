#encoding: utf-8

"""
Ce fichier est un exemple de fichier de configuration d'un test de benchmark

Pour l'utiliser, il suffit de le lancer via la commande `run' du shell afs

@author: Quentin
"""

# configuration du test de benchmark

# nom du test de benchmark (doit être identique au nom du fichier)
name = "example"

# commentaire éventuel sur le test
comment = "Example of benchmark tests"

# modules de test à lancer
# référez vous aux modules contenus dans le dossier modules/ pour remplir cette liste
modules = ["cp", "dd", "fdtree", "fileop", "iozone", "rsync"]

# liste des clients cibles du test
clients = {
    "localhost": {"path": "/srv", "times": 3} # lancement dans le pt de montage sur 3 threads
}

# spécifications sur le système de fichier testé
# ceci permet de créer un dossier comportant ces informations
fs = {
    "name": "rozofs",
    "version": "0.1"
}

# fin de configuration du test