#encoding: utf-8

"""

@author: Olivier
"""

import psutil
import time
import matplotlib
# Pour le support console sans serveur x
matplotlib.use('Agg')
from pylab import *



def getSysInfo():
    val = dict()
    val["time"] = time.time()
    val["mem"] = psutil.virtual_memory()[2]
    val["swap"] = psutil.swap_memory()[3]
    val["io"] = psutil.disk_io_counters(perdisk=False)
    val["net"] = psutil.network_io_counters(pernic=False)
    val["cpu"] = psutil.cpu_percent(interval=1)
    return val

def getSI(val=None):
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
    val["cpu"]      += [psutil.cpu_percent(interval=1)]
    return val

def timeRange(duration, inter=2):
    start = time.time()
    val = None
    while ((duration + start) - time.time()) > 0:
        val = getSI(val)
    return val

def graph(val=dict()):


    # x axis 
    dx = [int(i-val["time"][0]) for i in val["time"]]

    # Graphique pour le CPU, la RAM et le SWAP
    fig = figure()
    plt.ylabel('cpu(r) mem(b) swap(g) in %')
    plt.xlabel('time in sec')
    plt.plot(dx, val["cpu"], 'r-', dx, val["mem"], 'b-', dx, val["swap"], 'g-')
    fig.savefig('cpu_ram_swap.svg')

    # Graphique pour le disque
    fig = figure()
    plt.ylabel('Disk read(b) write(r) in Ko')
    plt.xlabel('time in sec')

    ior = []
    iow = []
    tmpr = val["io_read"][0]
    tmpw = val["io_write"][0]
    for r,w in zip(val["io_read"],val["io_write"]):
        ior += [r-tmpr]
        iow += [w-tmpw]
        tmpr = r
        tmpw = w

    # Passage byte à Ko
    iorf = [int((i/8)/1000) for i in ior]
    iowf = [int((i/8)/1000) for i in iow]

    plt.plot(dx, iorf, 'b-', dx, iowf, 'r-')
    fig.savefig('disk.svg')

    # Graphique pour le réseau
    fig = figure()
    plt.ylabel('Network sent(b) recv(r) in Ko')
    plt.xlabel('time in sec')

    nets = []
    netr = []
    tmps = val["net_sent"][0]
    tmpr = val["net_recv"][0]
    for s,r in zip(val["net_sent"],val["net_recv"]):
        nets += [s-tmps]
        netr += [r-tmpr]
        tmps = s
        tmpr = r

    # Passage byte à Ko
    netsf = [int((i/8)/1000) for i in nets]
    netrf = [int((i/8)/1000) for i in netr]

    plt.plot(dx, netsf, 'b-', dx, netrf, 'r-')
    fig.savefig('network.svg')
