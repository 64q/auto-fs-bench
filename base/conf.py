#encoding: utf-8

'''
Created on 26 févr. 2013

@author: Quentin
'''

import json

import ConfigParser


def load_config_all():
    """Charge toute la configuration"""
    
    config = ConfigParser.RawConfigParser()
    config.read("conf/app.cfg")
    
    return config


def load_config_app(param):
    """Charge la configuration de la section 'App'"""
    
    config = ConfigParser.RawConfigParser()
    config.read("conf/app.cfg")
    
    attr = config.get("App", param)
    
    return json.loads(attr)


def load_config_test(test):
    """Charge la configuration pour un test"""
    
    # configuration du parser
    config = ConfigParser.RawConfigParser()
    config.read("conf/" + test + ".cfg")
    
    conf = dict()
    
    # construction de la configuration
    conf["name"] = test
    conf["comment"] = config.get(test, "comment")
    conf["modules"] = json.loads(config.get(test, "modules"))
    conf["clients"] = json.loads(config.get(test, "clients"))
    conf["fs"] = json.loads(config.get(test, "fs"))
    
    return conf
