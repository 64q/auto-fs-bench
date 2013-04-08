# -*- coding: utf-8 -*-
"""
Module pour la gestion du test de benchmark : fdtree

Ce module utilise les scripts bash fdtree.sh et fdtree.bash
"""


import os, subprocess, stat
import core.errors

def test(workdir="./", var=""):
    valid = True
    text = ""

    if not os.path.isfile("bash-tools/fdtree.bash"):
        text += "bash-tools/fdtree.bash missing"
        valid = True
    else:
        os.chmod("bash-tools/fdtree.bash", stat.S_IWRITE | stat.S_IWRITE)
    
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
    p = subprocess.Popen(["/bin/bash", pos+"/bash-tools/fdtree.sh", var], cwd=workdir, stdout=subprocess.PIPE, env=penv)

    # Récupérer la sortie du process
    out, err = p.communicate()
    
    return out

def format(workdir="./", var=""):
    return ""

def graph(workdir="./", var=""):
    return ""

if __name__ == "__main__":
    # run("/tmp", "/srv")
    print test()
    os.system("pause")
