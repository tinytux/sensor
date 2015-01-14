#!/bin/bash
#
# 22.6.2014/cs
#

LOGSTASHVERSION="1.4.2"
WEB="-- web"

SCRIPTDIR="$(dirname "$0")"
cd ${SCRIPTDIR}
#LOGFILE=/var/log/logstash.log
LOGFILE=${SCRIPTDIR}/var/log/logstash.log
#PIDFILE=/var/run/logstash.pid
PIDFILE=${SCRIPTDIR}/var/run/logstash.pid


# .gitignore files make logstash fail. Remove them once:
# find vendor/ -name '.gitignore' -exec rm -v {} ';'


if [ ! -e bin ]; then
   echo "Extracting logstash..."
   tar --strip-components=1 -xvzf logstash-${LOGSTASHVERSION}.tar.gz logstash-${LOGSTASHVERSION}/vendor/kibana logstash-${LOGSTASHVERSION}/vendor/jar logstash-${LOGSTASHVERSION}/vendor/bundle logstash-${LOGSTASHVERSION}/lib logstash-${LOGSTASHVERSION}/spec logstash-${LOGSTASHVERSION}/locales logstash-${LOGSTASHVERSION}/bin
fi

echo "Running logstash v${LOGSTASHVERSION} on http://localhost:9292/ as user `whoami`..."

if [ ! -e $(dirname ${PIDFILE}) ]; then
    mkdir -p $(dirname ${PIDFILE})
fi
if [ ! -e $(dirname ${LOGFILE}) ]; then
    mkdir -p $(dirname ${LOGFILE})
fi
touch ${LOGFILE}
chmod o+rw ${LOGFILE}
GEM_HOME=${SCRIPTDIR}/vendor/bundle/jruby/2.1 /usr/bin/java -Djava.awt.headless=true \
         -jar ${SCRIPTDIR}/vendor/jar/jruby-complete-1.7.11.jar -I${SCRIPTDIR}/lib \
         ${SCRIPTDIR}/lib/logstash/runner.rb agent -w 4 -f ${SCRIPTDIR}/logstash.conf ${WEB} 2>&1 >${LOGFILE} &

echo $! >${PIDFILE}


# Restore SensorDashboard if needed
sleep 10
curl -s -X GET http://localhost:9200/kibana-int/dashboard/SensorDashboard/_source | grep SensorDashboard >/dev/null
if [[ $? -ne 0 ]]; then
    echo -n "Loading Kibana Dashboard..."
    sleep 10
    curl -X PUT http://localhost:9200/kibana-int/dashboard/SensorDashboard -T ./dashboards/SensorDashboard.json --silent
    echo 
fi
echo "Sensor Dashboard: http://localhost:9292/index.html#/dashboard/elasticsearch/SensorDashboard"


cd - >/dev/null


