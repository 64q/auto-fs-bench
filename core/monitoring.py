#encoding: utf-8

"""
Module permettant de gérer le monitoring des clients

@author: Olivier
"""

import os
import psutil
import time
import sys
import threading
import base64

import matplotlib

# Pour le support console sans serveur x
matplotlib.use('Agg')

from pylab import *


def getSysInfo():
    """
    Fonction basique pour récupérer quelques info système
    """

    val = dict()

    val["time"]     = [time.time()]
    val["mem"]      = [psutil.virtual_memory()[2]]
    val["swap"]     = [psutil.swap_memory()[3]]
    val["io_read"]  = [psutil.disk_io_counters(perdisk=False)[2]]
    val["io_write"] = [psutil.disk_io_counters(perdisk=False)[3]]
    val["net_sent"] = [psutil.network_io_counters(pernic=False)[0]]
    val["net_recv"] = [psutil.network_io_counters(pernic=False)[1]]
    val["cpu"]      = [psutil.cpu_percent(interval=0.8)]

    return val


def getSI(val=None):
    """
    Récupération de données système ajoutées dans uns liste

    Arguments:
    val -- métriques à acquérir
    """

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
    val["cpu"]      += [psutil.cpu_percent(interval=0.8)]

    return val


def timeRange(duration, inter=1):
    """
    Lancement de la récupération pour un temps défini

    Arguments:
    duration -- durée d'acquisition du monitoring
    inter -- intervalle d'acquisition
    """

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



def graph(val=dict(), prefix=""):
    """
    Création des graphiques associés aux résultats

    Arguments:
    val -- les métriques a prendre en compte
    prefix -- Chaine de caractères mise devant le nom 
            du fichier de monitoring. Peut être un dossier "/MyDir/"
    """

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

    size = floor(dx[len(dx)-1] / 60.0)
    if size < 15:
        size = 15

    # Création de la figure et des axes associés
    fig = figure(figsize=(size,20))
    ax1 = fig.add_axes([0.05, 0.69, 0.9, 0.28])
    ax2 = fig.add_axes([0.05, 0.36, 0.9, 0.28])
    ax3 = fig.add_axes([0.05, 0.03, 0.9, 0.28])

    # Graphique pour le CPU, la RAM et le SWAP
    ax1.set_ylabel('cpu - mem - swap (in %)')
    ax1.set_xlabel('time in seconde')
    ax1.set_title('CPU, RAM and SWAP Usage')
    lcpu, lmem, lswp = ax1.plot(dx, val["cpu"], 'r-', dx, val["mem"], 'b-', dx, val["swap"], 'y-')
    ax1.axis([0, dx[len(dx)-1], 0, 101])
    ax1.grid(True)
    ax1.axhline(0, color='black', lw=2)



    # GRafique pour le disque
    ax2.set_ylabel('Disk read - write (in Ko/sec)')
    ax2.set_xlabel('time in seconde')
    ax2.set_title('Disk Usage')

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
    iorf = [int(i/1024/1024) for i in ior]
    iowf = [int(u/1024/1024) for u in iow]

    lior, liow = ax2.plot(dx, iorf, 'b-', dx, iowf, 'r-')
    ax2.grid(True)
    ax2.axhline(0, color='black', lw=2)
    # Agencement du temps
    ax2.set_xlim(0,dx[len(dx)-1])


    # Graphique pour le réseau
    ax3.set_title('Network Usage')
    ax3.set_ylabel('Network incoming - outgoing (in Ko/sec)')
    ax3.set_xlabel('time in seconde')


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
    netsf = [int(i/1024/1024) for i in nets]
    netrf = [int(i/1024/1024) for i in netr]

    lnets, lnetr = ax3.plot(dx, netsf, 'r-', dx, netrf, 'b-')
    
    # Legend
    # fig.legend((lcpu, lmem,lswp, lior, liow, lnets, lnetr), \
    #     ('CPU', 'Memory', 'Swap', 'Disk read', 'Disk write', 'Network out', 'Network in'), 'right')

    fig.legend((lcpu, lmem,lswp), \
        ('CPU', 'Memory', 'Swap'), 'upper right')

    fig.legend((lior, liow), \
        ('Disk read', 'Disk write'), 'center right')

    fig.legend((lnets, lnetr), \
        ('Network out', 'Network in'), 'lower right')

    ax3.grid(True)
    ax3.axhline(0, color='black', lw=2)
    # Agencement du temps
    ax3.set_xlim(0,dx[len(dx)-1])

    # Ecriture du fichier du graphique
    fig.savefig(prefix+'monitoring.svg')
    fig.clf()


def graphFile(val=dict()):
    """
    Création du fichier du graphique

    Arguments:
    val -- métriques à acquérir
    """

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
        res[x] = base64.b64encode(f.read())
        f.close()
        os.remove('./'+rep+'/'+x)

    # suppression du dossier
    os.rmdir(rep)
    return res



class Monitoring(threading.Thread):
    """
    Récupération des résultats en arrière plan en threading
    """

    def __init__(self, inter=1):
        threading.Thread.__init__(self)
        self.val = None
        self.ok = True
        self.inter = inter
        self.Terminated = False

    def run(self):
        # Ajustement interval
        self.inter = round(self.inter)
        if self.inter < 1:
            self.inter = 1

        try:
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
        except:
            self.val = 0
            self.stop()
        return self.val

        sys.stdout.write("\n")
    
    def stop(self):
        self.Terminated = True
        while not self.ok:
            pass
        return self.val


