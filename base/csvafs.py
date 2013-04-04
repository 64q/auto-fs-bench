#encoding: utf-8

'''
Created on 4 avr. 2013

@author: Quentin
'''

import csv, time


def write_header(filename, test_conf, module):
    # ouverture du fichier en écriture
    csvfile = open(filename, "wb")
    
    # insertion du header de fichier CSV
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Resultats du module '%s'" %  module, time.strftime("%Y-%m-%d %H:%M:%S", test_conf["date"])])
    csvwriter.writerow([])
    csvfile.close()
