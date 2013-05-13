#encoding: utf-8

"""
Module de gestion des outils de benchmark, il s'occupe de charger les modules de benchmark et de
vérifier qu'ils sont correctement installés (avec les dépendances)

@author: Olivier
"""
 
import os
import threading
import time
import base64
import importlib

import core.errors


def modLoad(liste=None):
    """
    Chargement des modules selon une liste passée en paramètre, lève une exception si les modules ne
    passe pas la validation

    Arguments:
    liste -- liste des modules à charger
    """

    # Init
    mod = {}
    # Si liste vide, on charge tous les modules potentiels dans le dossier
    if liste is None:
        liste = []
        rep = os.listdir("./modules/")

        for r in rep :
            name = r[:-3]

            if os.path.isfile("./modules/"+r) and r[-3:] == ".py" and r[:2] != "__" and name != "":
                liste += [name]

    # parcours de la liste des modules
    for name in liste :
        try:
            # import du module
            module = importlib.import_module("modules." + name)

            # vérification des fonctions du module
            modCheck(module)

            # validation OK, on affecte les fonctions dans le dict
            mod[name] = val
        except core.errors.MissingFunctionError as e:
            raise core.errors.InvalidModuleError("Invalid module (function error: %s)" % e.__str__())
        except ImportError as e:
            raise core.errors.InvalidModuleError("Invalid module (import error: %s)" % e.__str__())

    return mod


def modCheck(mod):
    """
    Vérifier si un module contient toutes les fonctions nécessaires

    Arguments:
    mod -- le module à vérifier
    """

    func = ["test", "run"]
    #funcList = dir(modName)
    error = False
    for f in func:
        try:
            func = getattr(mod, f)
        except AttributeError as e:
            error = True
            raise core.errors.MissingFunctionError("fonction '%s' manquante" % f)

    return not error


def modLaunch(modfunc, func, param="", nb=1):
    """
    Lancement d'une instance d'une fonction d'un module

    Arguments:
    modfunc -- module cible
    func -- fonction cible du module
    param -- paramètres de lancement
    nb -- nombre de threads à lancer
    """

    # récupérer la fonction voulue
    pfonc = getattr(modfunc, func)
    
    # Sécurité sur le nombre de thread
    if nb < 1:
        nb = 1

    threads = [None] * nb
    results = dict()

    for i in range(nb):
        threads[i] = threading.Thread(None, context, None, (pfonc, results, 'thread_'+str(i), param))
        threads[i].start()

    for i in range(nb):
        threads[i].join()

    return results


def context(pfonc, result, name, param=""):
    """
    Fonction de contexte invoquée par les threads, cette fonction va créer un contexte d'execution
    unique pour le test afin d'éviter les collisions lors de l'execution de plusieurs threads

    Arguments:
    pfonc -- fonction executée
    result -- resultat d'execution
    name -- nom du thread
    param -- paramètres de lancement
    """

    val = 0
    ok = False
    while not ok:
        rep = 'exec_' + str(val)
        try:
            os.mkdir(rep)
            ok = True
        except OSError:
            val += 1
    # os.chdir(rep)
    
    # Appel de la fonction de bench
    # ajout du chemin du dossier réservé en premier paramètre
    result[name] = dict()
    result[name]['return'] = pfonc('./'+rep+'/', param)

    content = os.listdir(rep)

    # Ajouter les fichiers aux résultats
    tmp = dict()
    for x in content:
        f = open('./'+rep+'/'+x, 'r')
        tmp[x] = base64.b64encode(f.read())
        f.close()
    
    result[name]['files'] = tmp

    # vider le dossier
    for x in content:
        os.remove('./'+rep+'/'+x)
    os.rmdir(rep)


# test de la fonction table
if __name__ == "__main__":
    print "Modules :"
    mod = modLoad()
    # mod = modLoad(['du'])
    # mod['skeleton'].run()
    print ""
    print "Resultat :"
    print len(mod), "module(s) charge(s)"
    print mod.keys()
    res = modLaunch(mod['skeleton'], "run", nb=10)
    print res.keys()
    for k in res.keys():
        print k, ':'
        print '   return :', res[k]['return']
        print '   files  :'
        for kb in res[k]['files'].keys():
            print '     ',kb, '->', res[k]['files'][kb]
    # print os.getcwd()
    os.system("pause")