#encoding: utf-8

'''
Created on 4 avr. 2013

@author: Quentin
'''

class CmdError(Exception):
    """Exception lancée quand le retour d'une commande est invalide
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg