#!/bin/bash
#
# 22.6.2014/cs
#

SCRIPTDIR="$(dirname "${0}")"
cd ${SCRIPTDIR}
#PIDFILELS=/var/run/logstash.pid
PIDFILELS=${SCRIPTDIR}/var/run/logstash.pid


if [ -e ${PIDFILELS} ]; then
    echo "Stopping logstash..."
    cat ${PIDFILELS} | xargs kill -TERM
    RETVAL="$?"
    rm ${PIDFILELS}
else
    echo "logstash already stopped."
fi


# Shutdown local node
echo "Stopping elasticsearch..."
curl -s -XPOST 'http://localhost:9200/_cluster/nodes/_local/_shutdown' 2>&1  >/dev/null
if [ $? -eq 0 ]; then
    sleep 5
    echo "OK, node stopped."
else
    echo "FAILED, can not stop node."
fi


cd - >/dev/null
exit ${RETVAL}


