# -*- coding: utf-8 -*-
"""squelette de module de benchmark"""

import os

def test(workdir="./", var=""):
    return

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

def format(workdir="./", var=""):
    text = ""
    chaine = "0123456789OKMGokmg"
    for c in var:
        if c in chaine:
            text += c
        else:
            break
    return text

def graph(workdir="./", var=""):
    # import matplotlib
    # matplotlib.use('Agg')
    # from pylab import *
    # x = [-1, 0, 1, 2]
    # y = [3, 2, 4, 1]
    # plot(x, y)
    # savefig('fig.png')
    return

if __name__ == "__main__":
    run()
    print format(run())
    os.system("pause")
