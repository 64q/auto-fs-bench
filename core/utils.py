#encoding: utf-8

"""
Created on 4 avr. 2013

@author: Quentin
"""

import socket, json, csv, time
import threading, importlib


def threads_create_and_start(fn, params):
    thread = threading.Thread(target=fn, args=params)
    thread.start()

    return thread


def threads_join_all(threads):
    """
    Cette fonction permet de joindre tous les processus lancés
    """

    for t in threads:
        t.join()


def csv_write_header(filename, config, module):
    """
    Cette fonction permet d'écrire un petit header dans le fichier csv du module
    """

    # ouverture du fichier en écriture
    csvfile = open(filename, "wb")
    
    # insertion du header de fichier CSV
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Resultats du module '%s'" %  module, time.strftime("%Y-%m-%d %H:%M:%S", config.date)])
    csvwriter.writerow([])
    csvfile.close()


def csv_write_line(fp, line=[]):
    """
    Cette fonction permet d'écrire une ligne sur le fichier csv
    """

    # insertion du header de fichier CSV
    csvwriter = csv.writer(fp)
    csvwriter.writerow(line)


def load_config_client():
    """Charge la configuration du client"""
    
    return importlib.import_module('config.client')


def load_config_server():
    """Charge la configuration du serveur"""
    
    return importlib.import_module('config.server')


def load_config_test(test):
    """Charge la configuration pour un test"""
    
    return importlib.import_module('config.tests.' + test)
