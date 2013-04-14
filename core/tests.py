#encoding: utf-8

"""
Ce fichier contient des fonctions utilitaires pour la gestion des tests de bench


@author Quentin
"""

import core.utils
# import core.monitoring

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
                    fp.write(ct)
    
    # Création des graphiques associés
    # core.monitoring.graph(threads_results["monitoring"],  moduledir+"/"+client)
