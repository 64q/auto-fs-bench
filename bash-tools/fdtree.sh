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

. env.sh

#$1 mount point
#$2 levels
#$3 directories per level
#$4 files per directory
#$5 file size (in blocks 8k for rozofs)
#$6 file log
fdtree() {
	flog=${WORKING_DIR}/fdtree_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`_$2_$3_$4_$5.log
	${FDTREE_BINARY} -l $2 -d $3 -f $4 -s $5 -o $1 2>&1 | tee -a $flog
}

usage() {
	echo "$0: <mount point>"
	exit 0
}

[[ $# -lt 1 ]] && usage

[[ -z ${FDTREE_BINARY} ]] && echo "Can't find fdtree." && exit -1

fdtree $1 500 1 0 0
fdtree $1 1 20000 0 0
fdtree $1 1 1 20000 1
fdtree $1 6 5 6 1

exit 0
