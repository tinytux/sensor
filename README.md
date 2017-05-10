sensor
======

Humidity and temperature logger on Micro Python PYB v1.0

The humidity and temperature is recorded periodically (every 5 minutes) to a log file on the SD card.

## Micro Python data logger

Required hardware:
- Micro Python PYB v1.0
- Adafruit HIH6130 Humidity Sensor Breakout
- Adafruit 7-segment LED HT16K33 backpack

![image](sensor-micropython.jpg "Sensor with Micro Python PYB v1.0")

Source code: [micropython](micropython)

## Kibana Dashboard

Elasticsearch, Logstash and Kibana can be used to visualize the log data:

![screenshot](sensor-dashboard-screenshot.png "Sensor dashboard screenshot")

(A more advanced dashboard with Docker can be found [here](https://github.com/tinytux/solar-dashboard))

Usage on Debian Jessie 8:

    $ sudo apt-get install default-jre-headless curl
    $ git clone https://github.com/tinytux/sensor.git
    $ cd sensor/dashboard
    $ ./start.sh
    $ ./feedlogs.sh ./logdata/logdata.txt

Then visit [http://localhost:9292/index.html#/dashboard/elasticsearch/SensorDashboard](http://localhost:9292/index.html#/dashboard/elasticsearch/SensorDashboard)

Source code: [dashboard](dashboard)

