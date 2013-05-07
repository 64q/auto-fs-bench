# -*- coding: utf-8 -*-
"""
Script basique
"""

import os

import core.errors

def test():
    return True

def run(workdir="./", var=""):
    sortie=os.popen("du -sh "+var, "r").read()
    #fichier = open(workdir + "/res", "w")
    #fichier.write("hehe")
    #fichier.close()
    # os.remove('res')

    text = ""
    chaine = "0123456789OKMGokmg"
    for c in sortie:
        if c in chaine:
            text += c
        else:
            break

    return text


if __name__ == "__main__":
    print test()
    os.system("pause")
