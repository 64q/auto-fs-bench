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
# fdtree.sh 
#

WORKING_DIR=$PWD

# binaries
# if fdtree is in the PATH 
FDTREE_BINARY=`which fdtree.bash`
# if fdtree is in the PATH 
if [ -z "$FDTREE_BINARY" ]; then 
    FDTREE_BINARY=`which ./fdtree.bash`
fi

#$1 mount point
#$2 levels
#$3 directories per level
#$4 files per directory
#$5 file size (in blocks 8k for rozofs)
#$6 file log
fdtree() {
    flog=${WORKING_DIR}/fdtree_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`_$2_$3_$4_$5.log
    ${FDTREE_BINARY} -l $2 -d $3 -f $4 -s $5 -o $1 2>&1 | tee -a $flog

    # Clean errors in the file
    # rm
        # timer
        num=`wc -l $flog | cut -d' ' -f1`
        sed -i '/^rm: cannot remove .*: Timer expired$/d' $flog
        echo "rm - Timer expired :" $(($num - `wc -l $flog | cut -d' ' -f1`)) >> $flog

        # Autre 
        error=`grep -E "^rm: cannot remove " $flog | cut -d':' -f3 | sort -u`
        num=`wc -l $flog | cut -d' ' -f1`
        sed -i '/^rm: cannot remove /d' $flog
        echo "rm - autre erreur :" $(($num - `wc -l $flog | cut -d' ' -f1`)) >> $flog
        echo "Type autre erreur :" $error >> $flog


    # mkdir erreur
        # timer
        num=`wc -l $flog | cut -d' ' -f1`
        sed -i '/^mkdir: cannot create directory .*: Timer expired$/d' $flog
        echo "mkdir - Timer expired :" $(($num - `wc -l $flog | cut -d' ' -f1`)) >> $flog

        # Autre :
        error=`grep -E "^mkdir: cannot create directory " $flog | cut -d':' -f3 | sort -u`
        num=`wc -l $flog | cut -d' ' -f1`
        sed -i '/^mkdir: cannot create directory /d' $flog
        echo "mkdir - : autre erreur :" $(($num - `wc -l $flog | cut -d' ' -f1`)) >> $flog
        echo "Type autre erreur :" $error >> $flog

    # rmdir
        # Timer
        num=`wc -l $flog | cut -d' ' -f1`
        sed -i '/^rmdir: failed to remove .*: Timer expired$/d' $flog
        echo "rmdir - Timer expired :" $(($num - `wc -l $flog | cut -d' ' -f1`)) >> $flog

        # Autre
        error=`grep -E "^rmdir: failed to remove " $flog | cut -d':' -f3 | sort -u`
        num=`wc -l $flog | cut -d' ' -f1`
        sed -i '/^rmdir: failed to remove /d' $flog
        echo "rmdir - autre erreur :" $(($num - `wc -l $flog | cut -d' ' -f1`)) >> $flog
        echo "Type autre erreur :" $error >> $flog
}

usage() {
    echo "$0: <mount point>"
    exit 0
}

[[ $# -lt 1 ]] && usage

[[ -z ${FDTREE_BINARY} ]] && echo "Can't find fdtree." && exit -1

# Création du dossier de test
TESTDIR="$1/fdtree_${HOSTNAME}_$$"
mkdir $TESTDIR
if [ 0 -ne $? ]; then 
    echo "Error dir"
    exit 1
fi

# Test 1
fdtree $TESTDIR 500 1 0 0
rm -rf $TESTDIR/*
sleep 5

# Test 2
fdtree $TESTDIR 1 20000 0 0
rm -rf $TESTDIR/*
sleep 5

# Test 3
fdtree $TESTDIR 1 1 20000 1
rm -rf $TESTDIR/*
sleep 5

# Test 4
fdtree $TESTDIR 6 5 6 1

# fdtree $TESTDIR 3 3 2 1 # light test

rm -rf $TESTDIR

exit 0
