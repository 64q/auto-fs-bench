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

WORKING_DIR=$PWD
BONNIE_BINARY=`which bonnie++`

usage() {
	echo "$0: <mount point>"
	exit 0
}

[[ $# -lt 1 ]] && usage

[[ -z ${BONNIE_BINARY} ]] && echo "Can't find bonnie++." && exit -1

flog=${WORKING_DIR}/bonnie++_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`.log


# To put bonnie output in a file, use '2>&1 | tee $flog'
# ${BONNIE_BINARY} -d $1 -n 200 -m testedhost -s 16384 -f -u nobody 2>&1 | tee $flog
# ${BONNIE_BINARY} -d $1 -n 5 -s 16384 -f -u root 2>&1 | tee $flog
${BONNIE_BINARY} -d $1 -n 1 -s 4100 -f -u root -q 2>&1 | tee $flog # light test

exit 0
