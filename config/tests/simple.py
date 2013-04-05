#encoding: utf-8

"""
Ce fichier est un exemple de fichier de configuration d'un test de benchmark

Pour l'utiliser, il suffit de le lancer via la commande `run' du shell afs

@author Quentin
"""

# configuration du test de benchmark

# nom du test de benchmark (doit être identique au nom du fichier)
name = "simple"

# commentaire éventuel sur le test
comment = "Simple benchmark example"

# modules de test à lancer
modules = ["du"]

# liste des clients cibles du test
clients = {
    "client1": {"path": "./", "times": 3},
    "raspberry": {"path": "/home/drake", "times": 5}
}

# spécifications sur le système de fichier testé
fs = {
    "name": "rozofs",
    "version": "0.1"
}

# fin de configuration du test