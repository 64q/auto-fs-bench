#encoding: utf-8

"""
Ce fichier contient l'essentiel de la configuration de l'application.

Pour l'utiliser, il suffit de l'importer dans les fichiers source.

@author Quentin
"""

# configuration de l'application

# liste des clients de l'application
clients = dict(
    rozo1 = "192.168.100.1",
    rozo2 = "192.168.100.2",
    rozo3 = "192.168.100.3",
    rozo4 = "192.168.100.4",
    rozo5 = "192.168.100.5",
    rozo6 = "192.168.100.6",
    rozo7 = "192.168.100.7",
    rozo8 = "192.168.100.8"
)

# port d'envoi du serveur
send_port = 7979

# chemin des scripts de benchmark
scripts_dir = "bash-tools/"

# chemin des sauvegardes
save_dir = "data/"

# fin de configuration de l'application