#!/bin/bash
#
# Feed log files to logstash
#
# 22.6.2014/cs

LOGHOSTNAME="<unknown>"

LOGSTASHHOST="localhost"
LOGSTASHPORT=3333

if [[ $# -ne 1 ]]; then
    echo "usage: $0 [logfile]"
    echo -e "\n   example: $0 logdata/logdata.txt\n"
    exit 1
fi

FILE=${1}
if [[ ! -e ${FILE} ]]; then
    echo "File not found: >${FILE}<"
    exit 1
fi

LINECOUNT=`cat "${FILE}" | wc -l | tr -d '\n'`
if [[ ${LINECOUNT} -eq 0 ]]; then
    echo "No events in ${FILE}."
    exit 1
else
    echo "Feeding ${LINECOUNT} events from ${FILE} to logstash @ ${LOGSTASHHOST}:${LOGSTASHPORT}... (this takes more time)"
    # process all lines, use file descriptor 9 (not stdio/out)
    while read -r LINE <&9; do
        # remove white spaces from the beginning and end of line to allow reliable and simple pattern matching later
        TRIMLINE=`echo ${LINE} | tr '\t' ' ' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'`
        # use the MD5 sum as unique ID to avoid duplicates in the index
        MD5SUM=`echo ${TRIMLINE} | md5sum | cut -d ' ' -f 1` 
        # send to logstash
    echo "${MD5SUM} ${TRIMLINE}" | nc -q 5 ${LOGSTASHHOST} ${LOGSTASHPORT}
        if [[ $? -ne 0 ]]; then
        echo "${0} feed error. Exiting..."
        exit 1
    fi
    done 9< "${FILE}"
fi
                        
echo "${0} done: `date`"


