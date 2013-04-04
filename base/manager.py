#encoding: utf-8

'''
Created on 4 avr. 2013

@author: Quentin
'''

import os, time

import server
import base.conf, base.csvafs


def dirpath(conf_test):
    """
    Cette fonction permet de générer le chemin d'accès au dossier du projet
    et de créer le dossier
    """
    
    dirpath = server.Server.save_dir + conf_test["fs"]["name"] + "_" + conf_test["fs"]["version"] + "_" + conf_test["name"]
    
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        
    return dirpath


def filepath(test_conf, module):
    """
    Cette fonction génère le chemin vers le fichier .csv du module de test
    """
    
    return test_conf["dirpath"] + "/" + module + "_" + time.strftime("%Y%m%d_%H%M%S", test_conf["date"]) + ".csv"


def build_cl_config(conf_test, conf_client):
    """
    Construit la configuration du test chez le client
    """
    
    return {"path": conf_client["path"], "modules": conf_test["modules"], "times": conf_client["times"]}


def build_sv_config(test):
    """
    Construit la configuration du test chez le serveur
    """
    
    # chargement de la configuration de base
    test_conf = base.conf.load_config_test(test)
    
    test_conf["date"] = time.gmtime()
    test_conf["dirpath"] = base.manager.dirpath(test_conf)
    
    # création des fichiers de données
    for module in test_conf["modules"]:
        filename = filepath(test_conf, module)
        base.csvafs.write_header(filename, test_conf, module)
        
    return test_conf
