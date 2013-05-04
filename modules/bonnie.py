# -*- coding: utf-8 -*-
"""
Module pour la gestion du test de benchmark : bonnie++

Ce module utilise le script bash bonnie.sh
"""


import os, subprocess
import core.errors

def test():
    valid = True
    text = ""
    if subprocess.Popen(["which", "bonnie++"], stdout=subprocess.PIPE).communicate()[0] == "":
        text += " - bonnie++ missing"
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
    p = subprocess.Popen(["/bin/bash", pos+"/bash-tools/bonnie.sh", var], cwd=workdir, stdout=subprocess.PIPE)

    # Récupérer la sortie du process
    out, err = p.communicate()
    
    return "-"


if __name__ == "__main__":
    print test()
    os.system("pause")