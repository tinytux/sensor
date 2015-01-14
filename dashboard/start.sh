#!/bin/bash
#
# 22.6.2014/cs
#

SCRIPTDIR="$(dirname "${0}")"
cd ${SCRIPTDIR}

./runes.sh
sleep 2
./runlogstash.sh

cd - >/dev/null

