#encoding: utf-8

"""
Fichier de test de perf en montage local

@author Quentin
"""

# configuration du test de benchmark

# nom du test de benchmark (doit être identique au nom du fichier)
name = "raspberry-local"

# commentaire éventuel sur le test
comment = "test du systeme rozofs sur raspberry en local"

# modules de test à lancer
modules = ["dd"]

# liste des clients cibles du test
clients = {
    "rozo1": {"path": "/home/pi/raspberry-local", "times": 1}
    "rozo2": {"path": "/home/pi/raspberry-local", "times": 1}
    "rozo3": {"path": "/home/pi/raspberry-local", "times": 1}
    "rozo4": {"path": "/home/pi/raspberry-local", "times": 1}
    "rozo5": {"path": "/home/pi/raspberry-local", "times": 1}
    "rozo6": {"path": "/home/pi/raspberry-local", "times": 1}
    "rozo7": {"path": "/home/pi/raspberry-local", "times": 1}
    "rozo8": {"path": "/home/pi/raspberry-local", "times": 1}
}

# spécifications sur le système de fichier testé
fs = {
    "name": "rozofs",
    "version": "1.3.1"
}

# fin de configuration du test