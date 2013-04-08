# -*- coding: utf-8 -*-
"""
Module pour la gestion du test de benchmark : rsync

Ce module utilise les scripts bash rsync.sh et fdtree.bash
"""


import os, subprocess
import core.errors

def test(workdir="./", var=""):
    valid = True
    text = ""

    if subprocess.Popen(["which", "rsync"], stdout=subprocess.PIPE).communicate()[0] == "":
        text += " - /usr/bin/rsync missing"
        valid = False
    
    if not valid:
        raise core.errors.InvalidModuleError(text)
    return valid

def run(workdir="./", var=""):
    # Récupérer le dossier de travail courant
    pos = os.getcwd()

    # Add a new dir in the PATH
    penv = os.environ
    ee =  penv.copy().get("PATH",'')+":"+os.getcwd()+":"+os.getcwd()+"/bash-tools"
    penv["PATH"] = ee

    # Lancement du script bash
    #   interpréteur : /bin/bash
    #   chemin du script en dur
    #   passage des paramètres 'var'
    #   changement du dossier de travail
    p = subprocess.Popen(["/bin/bash", pos+"/bash-tools/rsync.sh", var], cwd=workdir, stdout=subprocess.PIPE, env=penv)

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