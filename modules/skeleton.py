# -*- coding: utf-8 -*-
"""
squelette de module de benchmark

Ce fichier donne la structure attendue pour un module
de benchmark. Il y a aussi quelques exemples de commandes
possibles.

"""

import os, subprocess, stat
import core.errors

def test():
    """
    Fonction pour vérifier que le script va pouvoir s'exécuter correctement
    sur le client.

    Si tout est OK, la fonction doit renvoyer TRUE.
    Dans le cas contraire il faut lancer une exception :
    raise core.errors.InvalidModuleError(TEXTE)

    Le répertoire courant est celui de lancement du programme :
        dossier "auto-fs-bench"
    """

    return True

def run(workdir="./", var=""):
    """
    Fonction d'exécution du test de benchmark.

    workdir : correspond au dossier où vous devez travailler. /!\ CE N'EST  PAS
        LE REPERTOIRE COURANT.
    var     : chemin du dossier monté à tester.

    Le répertoire courant est celui de lancement du programme :
        dossier "auto-fs-bench"

    """

    return "-"


if __name__ == "__main__":
    print test()
    os.system("pause")


"""
OUTILS :

Pour utiliser un script bash, utiliser la fonction subprocess.Popen :
    subprocess.Popen("./", bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)

Exemple :
    p = subprocess.Popen(["/bin/bash", "test.sh", workdir, var], cwd=workdir, stdout=subprocess.PIPE)
    out, err = p.communicate()

    cwd     : root le script dans le dossier de travaille
    stdout  : permet de récupérer la sortie standart et d'erreur.

Pour ajouter des informations dans le PATH du thread qui exécute le script bash (subprocess) :
    # Récupérer le dossier de travail courant
    pos = os.getcwd()

    # récupérer la variable d'environnement courrante
    penv = os.environ

    # Ajout des nouveaux chemins
    penv["PATH"] =  penv.copy().get("PATH",'')+":"+os.getcwd()+":"+os.getcwd()+"/bash-tools"

    # Appel de subprocess.Popen
    p = subprocess.Popen(["/bin/bash", pos+"/bash-tools/fdtree.sh", var], cwd=workdir, stdout=subprocess.PIPE, env=penv)

"""
