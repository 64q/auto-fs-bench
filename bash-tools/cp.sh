#!/bin/bash

#  Copyright (c) 2010 Fizians SAS. <http://www.fizians.com>
#  This file is part of Rozofs.
#  Rozofs is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published
#  by the Free Software Foundation, version 2.
#  Rozofs is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see
#  <http://www.gnu.org/licenses/>.

#
# cp.sh 
#

# Dossier de travail
WORKING_DIR=$PWD
# PID du thread pour la création du fichier commun sur un client
ROOT_FILENAME_TEST="file_$$"


#$1 mountpoint
do_cp()
{
    # Nom du fichier de sortie
    FILE_LOG=${WORKING_DIR}/cp_${$}_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`.log
    echo -e "size(MB)\t\tput(s)\tget(s)" > ${FILE_LOG}

    #for count in 1 10 100 1000 10000; do # adaptation pour test perso
    for count in 2 4 8 16 32 48 64 96 128 160; do
        # nom du fichier de travail
        FILENAME=${ROOT_FILENAME_TEST}_cp

        # Création d'un fichier de 1Mo * x dans le dossier de travail
        dd if=/dev/zero of=${WORKING_DIR}/${FILENAME} bs=$((1024*1024)) count=${count} >/dev/null 2>&1

        # PREMIER TEST : TPUT(S)
            # copie du fichier du dossier de travail vers le dossier monté
            echo -ne "${count}" >> ${FILE_LOG}
            echo -ne "\t\t`/usr/bin/time -f "%E" cp $WORKING_DIR/$FILENAME /$1 2>&1 | tr -d '\n'`" >> ${FILE_LOG}

            # Suppression du fichier du repertoire de travail
            rm -f $WORKING_DIR/$FILENAME

        # Tratement entre les actions put et Get
        sleep 1
        # Conflit pour l'exécution parallèle
        #sleep 3;umount ${1};sleep 3;mount ${1};sleep 3;

        # DEUXIEME TEST : TGET(S)
            echo -e "\t`/usr/bin/time -f "%E" cp $1/$FILENAME $WORKING_DIR/$FILENAME 2>&1 | tr -d '\n'`" >> ${FILE_LOG}

            # Suppression des fichiers
            rm -f $1/$FILENAME
            rm -f $WORKING_DIR/$FILENAME
    done;

    # Traitement des résultats
    mv ${FILE_LOG} "${FILE_LOG}.csv"
}

usage() {
    echo "$0: <mount point>"
    exit 0
}

[[ $# -lt 1 ]] && usage

do_cp $1

exit 0

