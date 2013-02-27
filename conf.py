#encoding: utf-8

'''
Created on 26 févr. 2013

@author: Quentin
'''

import json

def load(filename):
    try:
        # chargement du fichier de configuration
        fp = open(filename, 'r')
    except IOError:
        # fichier de configuration non trouve
        print "error: unable to open the specified config file '%s'" % filename
    
    return json.load(fp)
    