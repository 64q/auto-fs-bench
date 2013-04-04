# -*- coding: utf-8 -*-
"""module de gestion des outils de benchmark"""
 
import os
import threading
import time

def modLoad(liste = None):
    """Chargement des modules"""
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
            if modCheck(val) :
                mod[name] = val
            else :
                print '   erreur de fonction dans le module ', name

        except:
            print '   [except] erreur de langage dans le module ', name
    return mod

def modCheck(mod):
    """Vérifier si un module contient toutes les fonctions nécessaires"""
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
    """Lancement d'une instance d'une fonction d'un module"""
    # récupérer la fonction voulue
    pfonc = getattr(modfunc, func)
    
    # Sécurité sur le nombre de thread
    if nb < 1:
        nb = 1


    threads = [None] * nb
    results = [None] * nb

    for i in range(nb):
        threads[i] = threading.Thread(None, context, None, (pfonc, results, i, param))
        threads[i].start()

    for i in range(nb):
        threads[i].join()

    return results

def context(pfonc, result, number, param=""):
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
    result[number] = [pfonc('./'+rep+'/', param)]
    
    print "res>", pfonc('./'+rep+'/', param)

    content = os.listdir(rep)
    # Ajouter les fichiers aux résultats
    for x in content:
        tmp = [x]
        f = open('./'+rep+'/'+x, 'r')
        tmp += [f.read()]
        f.close()
        result[number] += [tmp]

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
    print modLaunch(mod['skeleton'], "run", nb=10)
    # print os.getcwd()
    # os.system("pause")