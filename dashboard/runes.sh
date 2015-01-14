#!/bin/bash
#
# 22.6.2014/cs
#

ELASTICSEARCHVERSION="1.1.1"


SCRIPTDIR="$(dirname "${0}")"
cd ${SCRIPTDIR}
#LOGFILE=/var/log/elasticsearch.log
LOGFILE=${SCRIPTDIR}/var/log/elasticsearch.log
#PIDFILE=/var/run/elasticsearch.pid
PIDFILE=${SCRIPTDIR}/var/run/elasticsearch.pid


if [ ! -e elasticsearch ]; then
    echo "Extracting elasticsearch..."
    mkdir elasticsearch
    tar --strip-components=1 -xvzf "elasticsearch-${ELASTICSEARCHVERSION}.tar.gz" --directory elasticsearch
    echo "Restoring log configuration file..."
    cp logging.yml elasticsearch/config/logging.yml
fi

# Keep ES in RAM. Add the following lines to "/etc/security/limits.conf" and reboot:
# *                hard    memlock         unlimited
# *                soft    memlock         unlimited
#ulimit -l unlimited
export ES_HEAP_SIZE=1024m

echo "Running elasticsearch v${ELASTICSEARCHVERSION} at http://localhost:9200/_search?pretty as user `whoami` with ${ES_HEAP_SIZE} heap..."

if [ ! -e $(dirname ${PIDFILE}) ]; then
    mkdir -p $(dirname ${PIDFILE})
fi
if [ ! -e $(dirname ${LOGFILE}) ]; then
    mkdir -p $(dirname ${LOGFILE})
fi
touch ${LOGFILE}
chmod o+rw ${LOGFILE}

./elasticsearch/bin/elasticsearch 2>&1 >${LOGFILE} &
echo $! >${PIDFILE}

cd - >/dev/null


