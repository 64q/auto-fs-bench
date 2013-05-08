#encoding: utf-8

"""
Ce fichier contient un ensemble de fonctions utilitaires pour manipuler des threads, du csv et bien
plus encore.

@author: Quentin
"""

import sys, socket, json, csv, time
import threading, importlib


def threads_create_and_start(fn, params=()):
    """
    Fonction permettant de créer un thread et de le démarrer

    Arguments:
    fn -- fonction à lancer dans le thread
    params -- tuple des paramètres additionnels à passer
    """

    thread = threading.Thread(target=fn, args=params)
    thread.start()

    return thread


def threads_join_all(threads):
    """
    Cette fonction permet de joindre tous les processus lancés

    Arguments:
    threads -- liste des threads
    """

    for t in threads:
        t.join()
        sys.stdout.flush()


def csv_write_header(filename, config, module):
    """
    Cette fonction permet d'écrire un petit header dans le fichier csv du module

    Arguments:
    filename -- fichier où enregistrer le header
    config -- configuration du test
    module -- module cible
    """

    # ouverture du fichier en écriture & insertion du header de fichier CSV
    with open(filename, "wb") as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(["Resultats du module '%s'" %  module, time.strftime("%Y-%m-%d %H:%M:%S", config.date)])
        csvwriter.writerow([])


def csv_write_line(fp, line=[]):
    """
    Cette fonction permet d'écrire une ligne sur le fichier csv

    Arguments:
    fp -- pointeur vers le fichier où enregistrer
    line -- ligne à écrire dans le fichier
    """

    # insertion du header de fichier CSV
    csvwriter = csv.writer(fp)
    csvwriter.writerow(line)


def load_config_client():
    """
    Charge la configuration du client
    """
    
    return importlib.import_module('config.client')


def load_config_server():
    """
    Charge la configuration du serveur
    """
    
    return importlib.import_module('config.server')


def load_config_test(test):
    """
    Charge la configuration pour un test

    Arguments:
    test -- test à charger en mémoire
    """
    
    return importlib.import_module('config.tests.' + test)


def print_title(content, ruler='-', underline=False):
    """
    Cette fonction permet de faire un peu de formattage en console

    Arguments:
    content -- contenu du titre
    ruler -- bordures du titre
    underline -- spécifie si le titre doit juste être souligné
    """

    if not underline:
        print "%s" % ruler * 70

    print content
    print "%s" % ruler * 70

def print_row(host, status, msg=""):
    """
    Affiche la ligne de manière tabulaire

    Arguments:
    host -- hôte
    status -- son état
    msg -- message additonnel
    """

    print " %-30s %-15s %-15s" % (host, status, msg)
