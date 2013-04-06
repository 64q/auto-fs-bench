# -*- coding: utf-8 -*-
"""
Module pour la gestion du test de benchmark : dd

Ce module utilise le script bash dd.sh
"""


import os, subprocess

def test(workdir="./", var=""):
    return True

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
    
    # sortie=os.popen("bash-tools/dd.sh "+workdir+" "+var, "r").read()
    return out

def format(workdir="./", var=""):
    return ""

def graph(workdir="./", var=""):
    return ""

if __name__ == "__main__":
    run("/tmp", "/srv")
    os.system("pause")