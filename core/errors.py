#encoding: utf-8

'''
Ce fichier contient toutes les erreurs lançables par l'application

@author: Quentin
'''

class CmdError(Exception):
    """
    Exception lancée quand le retour d'une commande est invalide
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class ClientTimeoutError(Exception):
    """
    Exception lancée quand le retour d'une commande est invalide
    """

    def __init__(self, msg):
        self.msg = msg


class ClientTransmissionError(Exception):
    """
    Exception lancée lorsque le retour du client est en erreur
    """

    def __init__(self, msg):
        self.msg = msg
