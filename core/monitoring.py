#encoding: utf-8

"""

@author: Olivier
"""

import os
import psutil
import time
import sys
import threading
import matplotlib
# Pour le support console sans serveur x
matplotlib.use('Agg')
from pylab import *



def getSysInfo():
    """Fonction basique pour récupérer quelques info système"""
    val = dict()
    val["time"]     = [time.time()]
    val["mem"]      = [psutil.virtual_memory()[2]]
    val["swap"]     = [psutil.swap_memory()[3]]
    val["io_read"]  = [psutil.disk_io_counters(perdisk=False)[2]]
    val["io_write"] = [psutil.disk_io_counters(perdisk=False)[3]]
    val["net_sent"] = [psutil.network_io_counters(pernic=False)[0]]
    val["net_recv"] = [psutil.network_io_counters(pernic=False)[1]]
    val["cpu"]      = [psutil.cpu_percent(interval=0.5)]
    return val


def getSI(val=None):
    """Récupération de données système ajoutées dans uns liste"""
    if val == None:
        val = dict()
        val["time"] = []
        val["mem"] = []
        val["swap"] = []
        val["io_read"] = []
        val["io_write"] = []
        val["net_sent"] = []
        val["net_recv"] = []
        val["cpu"] = []

    val["time"]     += [time.time()]
    val["mem"]      += [psutil.virtual_memory()[2]]
    val["swap"]     += [psutil.swap_memory()[3]]
    val["io_read"]  += [psutil.disk_io_counters(perdisk=False)[2]]
    val["io_write"] += [psutil.disk_io_counters(perdisk=False)[3]]
    val["net_sent"] += [psutil.network_io_counters(pernic=False)[0]]
    val["net_recv"] += [psutil.network_io_counters(pernic=False)[1]]
    val["cpu"]      += [psutil.cpu_percent(interval=0.5)]
    return val


def timeRange(duration, inter=1):
    """Lancement de la récupération pour un temps défini"""
    # Ajustement interval
    inter = round(inter)
    if inter < 1:
        inter = 1

    # Boucle de traitement
    start = time.time()
    val = None
    while ((duration + start) - time.time()) > 0:
        begin = time.time()
        val = getSI(val)
        diff = inter - (time.time() - begin)
        if diff < 0:
            diff = 0
        time.sleep(diff)
    return val



def graph(val=dict(), prefix = ''):
    """Création des graphiques associés aux résultats"""
    # Vérification qu'il y a des valeurs
    if not (type(val) == dict):
        return
    if not "time" in val.keys():
        return
    if not (len(val["time"]) > 1):
        return

    # reset
    plt.clf()

    # Création de la liste des temps
    dx = [int(round(i-val["time"][0])) for i in val["time"]]

    # Graphique pour le CPU, la RAM et le SWAP
    fig = figure(figsize=(20,10))
    plt.ylabel('red : cpu - blue : mem - green : swap (in %)')
    plt.xlabel('time in seconde')
    plt.title('CPU, RAM and SWAP Usage')
    plt.plot(dx, val["cpu"], 'r-', dx, val["mem"], 'b-', dx, val["swap"], 'g-')
    plt.axis([0, dx[len(dx)-1], 0, 100])
    fig.savefig(prefix+'_cpu_ram_swap.svg')
    plt.clf()

    # Graphique pour le disque
    fig = figure(figsize=(20,10))
    plt.ylabel('blue : read - red : write (in Ko/sec)')
    plt.xlabel('time in seconde')
    plt.title('Disk Usage')

    ior = []
    iow = []
    tmpr = val["io_read"][0]
    tmpw = val["io_write"][0]
    tmpt = val["time"][0] - 1
    for r,w,t in zip(val["io_read"], val["io_write"], val["time"]):
        ior += [(r-tmpr)/(t-tmpt)]
        iow += [(w-tmpw)/(t-tmpt)]
        tmpr = r
        tmpw = w
        tmpt = t

    # Passage byte à Ko
    iorf = [int(i/1000) for i in ior]
    iowf = [int(i/1000) for i in iow]

    plt.plot(dx, iorf, 'b-', dx, iowf, 'r-')
    fig.savefig(prefix+'_disk.svg')
    plt.clf()


    # Graphique pour le réseau
    fig = figure(figsize=(20,10))
    plt.ylabel('blue : outgoing - red : incoming (in Ko/sec)')
    plt.xlabel('time in seconde')
    plt.title('Network Usage')

    nets = []
    netr = []
    tmps = val["net_sent"][0]
    tmpr = val["net_recv"][0]
    tmpt = val["time"][0] - 1
    for s,r,t in zip(val["net_sent"], val["net_recv"], val["time"]):
        nets += [(s-tmps)/(t-tmpt)]
        netr += [(r-tmpr)/(t-tmpt)]
        tmps = s
        tmpr = r
        tmpt = t

    # Passage byte à Ko
    netsf = [int(i/1000) for i in nets]
    netrf = [int(i/1000) for i in netr]

    plt.plot(dx, netsf, 'b-', dx, netrf, 'r-')
    fig.savefig(prefix+'_network.svg')
    close()
    plt.clf()


def graphFile(val=dict()):
    # valeur de retour
    res = dict()

    # Création d'un dossier tmp
    num = 0
    ok = False
    while not ok:
        rep = 'tmp_' + str(num)
        try:
            os.mkdir(rep)
            ok = True
        except OSError:
            num += 1

    # Appel de la fonction graph()
    graph(val, rep+"/")

    # récupération des fichiers
    content = os.listdir(rep)
    for x in content:
        f = open('./'+rep+'/'+x, 'r')
        res[x] = f.read()
        f.close()
        os.remove('./'+rep+'/'+x)

    # suppression du dossier
    os.rmdir(rep)
    return res



class Monitoring(threading.Thread):
    """Récupération des résultats en arroère plan"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.val = None
        self.ok = True
        self.inter = 1
        self.Terminated = False

    def run(self):
        # Ajustement interval
        self.inter = round(self.inter)
        if self.inter < 1:
            self.inter = 1

        # Boucle de traitement
        while not self.Terminated:
            self.ok = False
            begin = time.time()
            self.val = getSI(self.val)
            diff = self.inter - (time.time() - begin)
            if diff < 0:
                diff = 0
            self.ok = True
            time.sleep(diff)
        return self.val

        sys.stdout.write("\n")
    
    def stop(self):
        self.Terminated = True
        while not self.ok:
            pass
        return self.val


