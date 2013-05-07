# -*- coding: utf-8 -*-
"""
Module pour la gestion du test de benchmark : pjdtest

Ce module utilise les scripts bash fdtree.sh et fdtree.bash
"""


import os, subprocess, stat
import core.errors

def test():
    valid = True
    text = ""

    if subprocess.Popen(["which", "gcc"], stdout=subprocess.PIPE).communicate()[0] == "":
        text += " - gcc missing"
        valid = False

    if subprocess.Popen(["which", "make"], stdout=subprocess.PIPE).communicate()[0] == "":
        text += " - make missing"
        valid = False

    if subprocess.Popen(["which", "prove"], stdout=subprocess.PIPE).communicate()[0] == "":
        text += " - prove missing"
        valid = False

    if valid:
        if not os.path.isfile("bash-tools/pjd-fstest-rozofs/fstest"):
            # Compilation du programme
            workdir = os.getcwd() + "/bash-tools/pjd-fstest-rozofs/"
            p = subprocess.Popen(["make"], cwd=workdir, stdout=subprocess.PIPE)
            out, err = p.communicate()

            # Vérifier si la compilation a fonctionné
            if not os.path.isfile("bash-tools/pjd-fstest-rozofs/fstest"):
                text += "Compilation FAIL : bash-tools/pjd-fstest-rozofs/fstest"
                valid = False

    if not valid:
        raise core.errors.InvalidModuleError(text)
    return valid

def run(workdir="./", var=""):
    # Récupérer le dossier de travail courant
    pos = os.getcwd()

    # Add a new dir in the PATH
    penv = os.environ
    ee =  penv.copy().get("PATH",'')+":"+os.getcwd()+":"+os.getcwd()+"/bash-tools/pjd-fstest-rozofs"
    penv["PATH"] = ee

    # Lancement du script bash
    #   interpréteur : /bin/bash
    #   chemin du script en dur
    #   passage des paramètres 'var'
    #   changement du dossier de travail
    p = subprocess.Popen(["/bin/bash", pos+"/bash-tools/pjdtest.sh", var], cwd=workdir, stdout=subprocess.PIPE, env=penv)

    # Récupérer la sortie du process
    out, err = p.communicate()
    
    return "-"


if __name__ == "__main__":
    print test()
    os.system("pause")
