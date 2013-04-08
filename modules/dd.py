# -*- coding: utf-8 -*-
"""
Module pour la gestion du test de benchmark : dd

Ce module utilise le script bash dd.sh
"""


import os, subprocess
import core.errors

def test(workdir="./", var=""):
    valid = True
    text = ""
    if subprocess.Popen(["which", "time"], stdout=subprocess.PIPE).communicate()[0] == "":
        text += " - /usr/bin/time missing"
        valid = False
    if subprocess.Popen(["which", "dd"], stdout=subprocess.PIPE).communicate()[0] == "":
        text += " - /bin/dd missing"
        valid = False

    if not valid:
        raise core.errors.InvalidModuleError(text)
    return valid

def run(workdir="./", var=""):
    # Récupérer le dossier de travail courant
    pos = os.getcwd()

    # Lancement du script bash
    #   interpréteur : /bin/bash
    #   chemin du script en dur
    #   passage des paramètres 'var'
    #   changement du dossier de travail
    p = subprocess.Popen(["/bin/bash", pos+"/bash-tools/dd.sh", var], cwd=workdir, stdout=subprocess.PIPE)

    # Récupérer la sortie du process
    out, err = p.communicate()
    
    return "-"

def format(workdir="./", var=""):
    return ""

def graph(workdir="./", var=""):
    return ""

if __name__ == "__main__":
    # run("/tmp", "/srv")
    print test()
    os.system("pause")