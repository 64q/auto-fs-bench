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
# dd.sh 
#

WORKING_DIR=$PWD
# PID process + timer to create uniq file on client
ROOT_FILENAME_TEST="file_${HOSTNAME}_$$_`date +%s%N`"

#$1 mountpoint
do_dd()
{
    # Ouput file name
    FILE_LOG=${WORKING_DIR}/dd_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`.log
    echo -e "size\tcount\tbs\twrite(s)\twrite(MB.s)\tread(s)\tread(MB.s)" >> ${FILE_LOG}

    # Start Test
    for bs in 4096 8192 16384; do
    # for bs in 4096 8192; do # light test
        #10Mo, 100Mo, 1Go, 10Go
        #10485760 104857600 1073741824 10737418240
        for size in 10485760 104857600 1073741824 10737418240 ; do
        # for size in 40960 81920 163840 327680 ; do # light test

            # Number of blocks
            let count=${size}/${bs}

            # Test file name
            FILENAME=${ROOT_FILENAME_TEST}_${size}_${count}_${bs}

            # local to mount dir
                echo -ne "${size}\t${count}\t${bs}" >> ${FILE_LOG}
                result=`dd conv=fdatasync if=/dev/zero of=$1/${FILENAME} bs=${bs} count=${count} 2>&1 | tail -n +3 | tr -s ' '`
                time=`echo $result | cut -d ' ' -f 6`
                rate=`echo $result | cut -d ' ' -f 8`
                echo -ne "\t$time\t$rate" >> ${FILE_LOG}

            # Tempo between put and Get action
            sleep 5
            # Conflit pour l'exécution parallèle
            #sleep 3;umount ${1};sleep 3;mount ${1};sleep 3;

            # mount dir to local
                result=`dd conv=fdatasync of=/dev/null if=${1}/${FILENAME} bs=${bs} count=${count} 2>&1 | tail -n +4 | tr -s ' '`
                time=`echo $result | cut -d ' ' -f 6`
                rate=`echo $result | cut -d ' ' -f 8`
                echo -e "\t$time\t$rate" >> ${FILE_LOG}

            # delete created files
            rm -f ${1}/${FILENAME} 2>&1
        done;
    done;

    # results treatment
    #sed -i 's/\,/\./g' ${FILE_LOG}
    mv ${FILE_LOG} "${FILE_LOG}.csv"
}

usage() {
    echo "$0: <mount point>"
    exit 0
}

[[ $# -lt 1 ]]  && usage

do_dd $1

exit 0

