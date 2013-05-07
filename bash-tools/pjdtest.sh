#!/bin/bash

#  Copyright (c) 2010 Fizians SAS. <http://www.fizians.com>
#  This file is part of Rozofs.
#
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
# pjdtest.sh 
#

WORKING_DIR=$PWD
LOCAL_PJDTESTS=`which fstest`
LOCAL_DIR=`dirname ${LOCAL_PJDTESTS}`

[[ -z ${LOCAL_PJDTESTS} ]] && echo "Can't find pjdtest." && exit -1

#$1 mount point
pjdtest() {

    # Path for the log file
    flog=${WORKING_DIR}/pjdtest_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`.log

    # Go to mountpoint
    cd $1

    # EXECUTE FILEOP
    prove -r ${LOCAL_DIR} 2>&1 | tee -a $flog

    # Return to current directory
    cd ${WORKING_DIR}
}

usage() {
    echo "$0: <mount point>"
    exit 0
}

[[ $# -lt 1 ]] && usage

pjdtest $1

exit 0
