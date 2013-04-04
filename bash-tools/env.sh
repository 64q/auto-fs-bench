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

NAME_LABEL="$(uname -a)"
DATE_LABEL="$(date +%d-%m-%Y-%H:%M:%S)"
WORKING_DIR=$PWD

# binaries
FDTREE_BINARY=${WORKING_DIR}/fdtree.bash
FSOP_BINARY=`which fileop`
IOZONE_BINARY=`which iozone`
RSYNC_BINARY=`which rsync`
BONNIE_BINARY=`which bonnie++`
GNUPLOT_BINARY=`which gnuplot`

