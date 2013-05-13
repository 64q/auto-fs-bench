#encoding: utf-8

"""
Ce fichier contient toutes les erreurs lançables par l'application

@author: Quentin
"""

class CmdError(Exception):
    """
    Exception lancée quand le retour d'une commande est invalide
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

    def __str__(self):
        return self.msg


class ClientTimeoutError(Exception):
    """
    Exception lancée quand le retour d'une commande est invalide
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ClientTransmissionError(Exception):
    """
    Exception lancée lorsque le retour du client est en erreur
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidModuleError(Exception):
    """
    Exception lancée lorsque le module est invalide
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class TestsError(Exception):
    """
    Exception lancée lorsque les tests échouent
    """

    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg

class UnknownClientError(Exception):
    """
    Exception lancée lorsque le client est inconnu
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class MissingFunctionError(Exception):
    """
    Exception lancée lorsque la fonction du module est absente
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
