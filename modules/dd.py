# -*- coding: utf-8 -*-
"""Fonction dd de module de benchmark"""

import os

def test(workdir="./", var=""):
    return True

def run(workdir="./", var=""):
    sortie=os.popen("bash-tools/dd.sh "+workdir+" "+var, "r").read()
    return sortie

def format(workdir="./", var=""):
    return ""

def graph(workdir="./", var=""):
    return ""

if __name__ == "__main__":
    os.system("pause")