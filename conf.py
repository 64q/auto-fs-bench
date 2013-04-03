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
    config.read("app.cfg")
    
    return config

def load_config_app(param):
    """Charge la configuration de la section 'App'"""
    
    config = ConfigParser.RawConfigParser()
    config.read("app.cfg")
    
    attr = config.get("App", param)
    
    return json.loads(attr)

def load_config_module(module):
    """Charge la configuration de la section 'Modules'"""
    
    config = ConfigParser.RawConfigParser()
    config.read("app.cfg")
    
    attr = config.get("Modules", module)
    
    return json.loads(attr)