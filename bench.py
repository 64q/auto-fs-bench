# -*- coding: utf-8 -*-
"""module de gestion des outils de benchmark"""
 
import os

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
    os.system("pause")