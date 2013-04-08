#encoding: utf-8

"""
Ce fichier contient un ensemble de fonctions utiles pour manipuler les configurations de test

@author: Quentin
"""

import os, time

import core.utils


def generate_filename(config, module):
    """
    Cette fonction génère le nom du fichier de sauvegarde de la sortie du script de bench
    """

    # chargement du dirname du module
    dirname = generate_moduledir(config, module)

    return dirname + "/" + module + "_" + time.strftime("%Y%m%d_%H%M%S", config.date) + ".csv"


def generate_testdir(test_config):
    """
    Cette fonction génère le dossier du test
    """

    # chargement de la configuration et génération dirname
    config = core.utils.load_config_server()
    dirname = config.save_dir + "/" + test_config.name + "_" + test_config.fs["name"] + "_" \
        + test_config.fs["version"] + "_" + time.strftime("%Y%m%d_%H%M%S", test_config.date)

    # le dossier est créé uniquement s'il n'existe pas
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    return dirname


def generate_moduledir(config, module):
    """
    Cette fonction génère le dossier de sauvegarde des résultats s'il n'existe pas

    Sinon, il retourne le chemin du dossier correspondant
    """

    # chargement de la configuration et génération dirname
    dirname = config.dirpath + "/" + module

    # le dossier est créé uniquement s'il n'existe pas
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    return dirname


def build_client_config(config, client, module):
    """
    Construit la configuration du test chez le client
    """
    
    # création config client
    client_config = dict(
        path = config.clients[client]["path"],
        module = module,
        times = config.clients[client]["times"]
    )

    return client_config


def build_server_config(test):
    """
    Construit la configuration du test chez le serveur
    """
    
    # chargement de la configuration de base
    config = core.utils.load_config_test(test)
    
    # ajout des variables de configuration supplémentaires
    setattr(config, "date", time.gmtime())
    setattr(config, "dirpath", core.manager.generate_testdir(config))
    
    # création des fichiers de données avec header
    for module in config.modules:
        filename = generate_filename(config, module)
        core.utils.csv_write_header(filename, config, module)
        
    return config
