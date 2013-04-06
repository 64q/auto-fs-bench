# -*- coding: utf-8 -*-
"""squelette de module de benchmark"""

import os

def test(workdir="./", var=""):
    print("sketest")
    return True

def run(workdir="./", var=""):
    fichier = open(workdir+"res", "w")
    fichier.write('-file-\n'+workdir) 
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



# Pour appeler un script bash :
# subprocess.Popen("./", bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)
# p = subprocess.Popen(["/bin/bash", pos+"/test.sh", workdir, var], cwd="/tmp", stdout=subprocess.PIPE)
# out, err = p.communicate()