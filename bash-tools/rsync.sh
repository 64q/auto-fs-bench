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

. env.sh

	
usage() {
	echo "$0: <mount point>"
	exit 0
}

[[ $# -lt 1 ]] && usage

[[ -z ${RSYNC_BINARY} ]] && echo "Can't find rsync." && exit -1
[[ -z ${FDTREE_BINARY} ]] && echo "Can't find fdtree." && exit -1

flog=${WORKING_DIR}/rsync_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`.log
tmpd="/tmp/$$"

mkdir $tmpd
echo "Begin fdtree: $(date +%d-%m-%Y--%H:%M:%S)" >> $flog
${FDTREE_BINARY} -C -l 3 -d 15 -f 15 -s 2 -o $tmpd 2>&1 | tee -a $flog
echo "End fdtree and begin rsync: $(date +%d-%m-%Y--%H:%M:%S)" >> $flog
time ${RSYNC_BINARY} -avz $tmpd $1 2>&1 | tee -a $flog
echo "End rsync and Begin rm: $(date +%d-%m-%Y--%H:%M:%S)" >> $flog
time rm -rf $1/* 2>&1 | tee -a $flog
echo "End rm: $(date +%d-%m-%Y--%H:%M:%S)" >> $flog
exit 0
