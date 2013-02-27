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

. env.sh

ROOT_FILENAME_TEST=file_test

#$1 mountpoint
do_cp()
{
    FILE_LOG=${WORKING_DIR}/cp_`date "+%Y%m%d_%Hh%Mm%Ss"`_`basename $1`.log
	echo -e "size(KB)\t\tput(s)\tget(s)" > ${FILE_LOG}
	for count in 1000 10000 100000 1000000 10000000; do
		FILENAME=file_test
		dd if=/dev/zero of=${FILENAME} bs=1024 count=${count} >/dev/null 2>&1

		echo -ne "${count}" >> ${FILE_LOG}
		echo -ne "\t\t`/usr/bin/time -f "%E" cp $FILENAME /$1 2>&1 | tr -d '\n'`" >> ${FILE_LOG}
		rm -f ${FILENAME}
		sleep 3;umount ${1};sleep 3;mount ${1};sleep 3;
		echo -e "\t`/usr/bin/time -f "%E" cp $1/$FILENAME . 2>&1 | tr -d '\n'`" >> ${FILE_LOG}
		rm -f ${1}/${FILENAME}
	done;

}

usage() {
	echo "$0: <mount point>"
	exit 0
}

[[ $# -lt 1 ]] && usage

do_cp $1

exit 0

