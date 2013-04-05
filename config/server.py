#encoding: utf-8

"""
Ce fichier contient l'essentiel de la configuration de l'application.

Pour l'utiliser, il suffit de l'importer dans les fichiers source.

@author Quentin
"""

# configuration de l'application

# liste des clients de l'application
clients = dict(
    client1 = "127.0.0.1",
    client2 = "192.168.0.10"
)

# port d'envoi du serveur
send_port = 7979

# chemin des scripts de benchmark
scripts_dir = "bash-tools/"

# chemin des sauvegardes
save_dir = "data/"

# fin de configuration de l'application