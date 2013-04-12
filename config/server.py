#encoding: utf-8

"""
Ce fichier contient l'essentiel de la configuration de l'application.

Pour l'utiliser, il suffit de l'importer dans les fichiers source.

@author Quentin
"""

# configuration de l'application

# liste des clients de l'application
clients = dict(
    localhost = "127.0.0.1",
    servoliv = "192.168.0.50",
    raspberry = "192.168.0.3",
    ptrans1 = "10.0.2.51",
    ptrans2 = "10.0.2.53",
    ptrans3 = "10.0.2.52",
    rozo1 = "1.1.100.11",
    rozo2 = "1.1.100.21",
    rozo3 = "1.1.100.31",
    rozo4 = "1.1.100.41",
    rozo5 = "1.1.100.51",
    rozo6 = "1.1.100.61",
    rozo7 = "1.1.100.71",
    rozo8 = "1.1.100.81",
    rozo9 = "1.1.100.91",
    rozo10 = "1.1.100.101",
    rozo11 = "1.1.100.111",
    rozo12 = "1.1.100.121"
)

# port d'envoi du serveur
send_port = 7979

# chemin des scripts de benchmark
scripts_dir = "bash-tools/"

# chemin des sauvegardes
save_dir = "data/"

# fin de configuration de l'application