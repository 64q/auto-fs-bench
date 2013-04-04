# -*- coding: utf-8 -*-
"""squelette de module de benchmark"""

import os

def test(workdir="./", var=""):
    print("sketest")
    return "sketest"

def run(workdir="./", var=""):
    fichier = open(workdir+"res", "w")
    fichier.write('Youpi !!!!!!!\n'+workdir) 
    fichier.close()
    # os.remove('res')
    print("skerun")
    return "skerun"

def format(workdir="./", var=""):
    print("skeformat")
    return "skeformat"

def graph(workdir="./", var=""):
    print("skegraph")
    return "skegraph"

if __name__ == "__main__":
    os.system("pause")