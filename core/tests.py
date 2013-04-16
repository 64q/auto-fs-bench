#encoding: utf-8

"""
Ce fichier contient des fonctions utilitaires pour la gestion des tests de bench


@author Quentin
"""

import json
import base64

import core.utils

def save_files(moduledir, filename, client, threads_results):
    """
    Cette fonction créé les fichiers correspondant aux tests effectués du module
    """

    with open(filename, "ab") as csvfile:
        for thread_id, thread_content in threads_results["returnValue"].iteritems():
            # écriture de la ligne de résultat 'return'
            core.utils.csv_write_line(csvfile, 
                [client + "_" + thread_id, thread_content["return"]])

            # création des fichiers de sortie du module de benchmark
            for fn, ct in thread_content["files"].iteritems():
                with open(moduledir + "/" + client + "_" + thread_id + "_" + fn, "w") as fp:
                    fp.write(base64.b64decode(ct))

        # Récupération des fichiers de monitoring
        if "monitoring" in threads_results.keys():
            for mon_elem, mon_res in threads_results["monitoring"].iteritems():
                with open(moduledir + "/_" + client + "_" + mon_elem, "w") as fp:
                    fp.write(base64.b64decode(mon_res))

