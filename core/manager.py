#encoding: utf-8

"""
Ce fichier contient un ensemble de fonctions utiles pour manipuler les configurations de test

@author: Quentin
"""

import os, time

import core.utils


def generate_filename(config, module, virtual=False):
    """
    Cette fonction génère le nom du fichier de sauvegarde de la sortie du script de bench

    Arguments:
    config -- configuration du test de benchmark
    module -- module ciblé
    virtual -- indique si le fichier doit être créé physiquement ou pas
    """

    # chargement du dirname du module
    dirname = generate_moduledir(config, module, virtual)

    return dirname + "/" + module + "_" + time.strftime("%Y%m%d_%H%M%S", config.date) + ".csv"


def generate_testdir(test_config, virtual=False):
    """
    Cette fonction génère le dossier du test

    Arguments:
    test_config -- configuration du test de benchmark
    virtual -- indique si le dossier doit être créé physiquement ou pas
    """

    # chargement de la configuration et génération dirname
    config = core.utils.load_config_server()
    dirname = config.save_dir + "/" + test_config.name + "_" + test_config.fs["name"] + "_" \
        + test_config.fs["version"] + "_" + time.strftime("%Y%m%d_%H%M%S", test_config.date)

    # le dossier est créé uniquement s'il n'existe pas
    if not virtual and not os.path.exists(dirname):
        os.mkdir(dirname)

    return dirname


def generate_moduledir(config, module, virtual=False):
    """
    Cette fonction génère le dossier de sauvegarde des résultats s'il n'existe pas sinon, il 
    retourne le chemin du dossier correspondant

    Arguments:
    config -- configuration du test
    module -- module du test ciblé
    virtual -- indique si le dossier doit être créé physiquement ou pas
    """

    # chargement de la configuration et génération dirname
    dirname = config.dirpath + "/" + module

    # le dossier est créé uniquement s'il n'existe pas
    if not virtual and not os.path.exists(dirname):
        os.mkdir(dirname)

    return dirname


def build_client_config(config, client, module):
    """
    Construit la configuration du test chez le client

    Arguments:
    config -- configuration du serveur
    client -- client cible de la création de la config
    module -- le module à inclure dans la config
    """
    
    # création config client
    client_config = dict(
        path = config.clients[client]["path"],
        module = module,
        times = config.clients[client]["times"]
    )

    return client_config


def build_server_config(test, virtual=False):
    """
    Construit la configuration du test chez le serveur

    Arguments:
    test -- test de benchmark à charger
    virtual -- indique si la construction implique la création de l'arborescence ou pas (utile si
    on désire juste tester la config)
    """
    
    # chargement de la configuration de base
    config = core.utils.load_config_test(test)
    
    # ajout des variables de configuration supplémentaires
    setattr(config, "date", time.gmtime())
    setattr(config, "dirpath", core.manager.generate_testdir(config, virtual=virtual))
    
    # création des fichiers de données avec header
    for module in config.modules:
        filename = generate_filename(config, module, virtual=virtual)

        if not virtual:
            core.utils.csv_write_header(filename, config, module)
        
    return config
