# -*- coding: utf-8 -*-
"""module de gestion des outils de benchmark"""
 
import os
import threading
import time
import base64

import core.errors


def modLoad(liste = None):
    """
    Chargement des modules
    """

    # Init
    mod = {}
    # Si liste vide, on charge tous les modules potentiels dans le dossier
    if liste == None:
        liste = []
        rep = os.listdir("./modules/")
        print rep
        for r in rep :
            name = r[:-3]
            print name
            if os.path.isfile("./modules/"+r) and r[-3:] == ".py" and r[:2] != "__" and name != "":
                liste += [name]


    print "liste", liste
    # parcours de la liste des modules
    for name in liste :
        print 'Chargement du module', name

        try:
            res = __import__("modules."+name)
            val = getattr(res, name)
            # val = importlib.import_module('modules.'+name)
            if modCheck(val) :
                mod[name] = val
            else :
                print '   erreur de fonction dans le module ', name
                raise InvalidModuleError("Invalid module (function error)")

        except:
            print '   [except] erreur de langage dans le module ', name
            raise core.errors.InvalidModuleError("Invalid module (language error)")
    return mod


def modCheck(mod):
    """
    Vérifier si un module contient toutes les fonctions nécessaires
    """

    func = ["test", "run", "format", "graph"]
    #funcList = dir(modName)
    error = False
    for f in func:
        try:
            func = getattr(mod, f)
        except AttributeError:
            error = True
            print '   fonction', f, 'manquante'
    return not error


def modLaunch(modfunc, func, param="", nb=1):
    """
    Lancement d'une instance d'une fonction d'un module
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