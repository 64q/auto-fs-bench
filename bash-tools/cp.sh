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

WORKING_DIR=$PWD
# PID process + timer to create uniq file on client
ROOT_FILENAME_TEST="file_${HOSTNAME}_$$_`date +%s%N`"


#$1 mountpoint
do_cp()
{
    # Ouput file name
    FILE_LOG=${WORKING_DIR}/cp_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`.log
    echo -e "size(MB)\t\tput(s)\tget(s)" > ${FILE_LOG}

    # for count in 1 10 100 1000 10000; do
    for count in 2 4 8 16 32 48 64 96 128 160; do # light test
        # work file name
        FILENAME=${ROOT_FILENAME_TEST}_cp

        # Create a file of 1Mo * x in the workdir
        dd if=/dev/zero of=${WORKING_DIR}/${FILENAME} bs=$((1024*1024)) count=${count} >/dev/null 2>&1

        # FIRST TEST : TPUT(S)
            # work dir to mount dir
            echo -ne "${count}" >> ${FILE_LOG}
            echo -ne "\t\t`/usr/bin/time -f "%E" cp $WORKING_DIR/$FILENAME /$1 2>&1 | tr -d '\n'`" >> ${FILE_LOG}

            # delete file in the work dir
            rm -f $WORKING_DIR/$FILENAME

        # Tempo between put and Get action
        sleep 5
        # Conflit pour l'exécution parallèle
        #sleep 3;umount ${1};sleep 3;mount ${1};sleep 3;

        # SECOND TEST : TGET(S)
            echo -e "\t`/usr/bin/time -f "%E" cp $1/$FILENAME $WORKING_DIR/$FILENAME 2>&1 | tr -d '\n'`" >> ${FILE_LOG}

            # delete files
            rm -f $1/$FILENAME
            rm -f $WORKING_DIR/$FILENAME
    done;

    # results treatment
    mv ${FILE_LOG} "${FILE_LOG}.csv"
}

usage() {
    echo "$0: <mount point>"
    exit 0
}

[[ $# -lt 1 ]] && usage

do_cp $1

exit 0

