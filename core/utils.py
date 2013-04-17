#encoding: utf-8

"""
Created on 4 avr. 2013

@author: Quentin
"""

import sys, socket, json, csv, time
import threading, importlib

import server


def threads_create_and_start(fn, params=()):
    thread = threading.Thread(target=fn, args=params)
    thread.start()

    return thread


def threads_join_all(threads):
    """
    Cette fonction permet de joindre tous les processus lancés
    """

    for t in threads:
        t.join()
<<<<<<< HEAD
        print "Thread %s terminé !" % t.name
=======
        sys.stdout.flush()
>>>>>>> e33cafe614a28db5792aecabfab78aa53cd09d1b


def csv_write_header(filename, config, module):
    """
    Cette fonction permet d'écrire un petit header dans le fichier csv du module
    """

    # ouverture du fichier en écriture & insertion du header de fichier CSV
    with open(filename, "wb") as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(["Resultats du module '%s'" %  module, time.strftime("%Y-%m-%d %H:%M:%S", config.date)])
        csvwriter.writerow([])


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


def print_title(content, ruler='-'):
    print "%s" % ruler * 70
    print content
    print "%s" % ruler * 70

class LoadingBarThread(threading.Thread):
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.nom = nom
        self.Terminated = False
    def run(self):
        while not self.Terminated:
            time.sleep(0.5) # do real work here
            # update the bar
            sys.stdout.write(".")
            sys.stdout.flush()

        sys.stdout.write("\n")
    def stop(self):
        self.Terminated = True
