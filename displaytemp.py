#
# Humidity and temperature logger on Micro Python PYB v1.0
#
# The humidity and temperature is recorded periodically (every 5 minutes) to a log file
# on the SD card.
#

from pyb import RTC, I2C, Switch
from time import sleep
from sevensegment import SevenSegment
from humiditytemperature import HumidityTemperature
import os


def writeLog(rtc, values):
    """Append a line with the current timestamp to the log file"""
    datetime=rtc.datetime()
    timestamp = ("%04d-%02d-%02d %02d:%02d:%02d" % (datetime[0], datetime[1], datetime[2], datetime[4], datetime[5], datetime[6]))
    logline = ("%s %s" % (timestamp, values))

    # BLUE: I/O
    pyb.LED(4).on()
    print(logline)
    try:
        with open("/sd/logdata.txt", "a") as f:
            f.write("%s\n" % logline)
            f.close()
            pyb.sync()

        # GREEN: OK
        pyb.LED(2).on()
        sleep(2)
        pyb.LED(2).off()
    except OSError as error:
        # RED: ERROR
        pyb.LED(1).on()
        print("Error: can not write to SD card. %s" % error)
        sleep(2)
        pyb.LED(1).off()
    pyb.LED(4).off()


# the USR button can be used to toggle the display mode (temperature, humidity, off)
displayMode = 0
def buttonPressed():
    """User Button pressed"""
    global displayMode
    displayMode = ((displayMode + 1) % 3) 


sw = Switch()
sw.callback(buttonPressed)

i2c = I2C(1)
i2c.init(I2C.MASTER)

display = SevenSegment(i2c)
humtemp = HumidityTemperature(i2c)

rtc = RTC()
year, month, day, weekday, hour, minute, second, millisecond = rtc.datetime()

# show the date at startup if the RTC is not set
if year < 2015:
  print("RTC setup required: rtc.datetime((2014, 10, 12, 7, 17, 30, 0, 0))")
  print("Run under Linux: date +\"rtc.datetime((%Y, %m, %d, %u, %H, %M, %S, 00))\"")
  display.blink(True)
  display.write("%02d.%02d" % (day, month))
  sleep(2)
  display.write("%4d" % (year))
  sleep(2)
  display.blink(False)


# reduce frequency to save power (supported MHz: 8, 16, 24, 30, 32, 36, 40, 42, 48, 54, 56, 60, 64, 72, 84, 96, 108, 120, 144, 168)
# Note: do not go below 64 MHz or writing to the SD card will fail with errno 5
pyb.freq(64 * 1000000)

loopCounter = 0
while True:
    humidity = humtemp.humidity()
    temperature =  humtemp.temperature()

    # USR Switch toggles output
    if displayMode == 0:
        display.enable(True)
        display.write("%0.02f" % (temperature))
    elif displayMode == 1:
        display.write("%0.02f" % (humidity))
    else:
        display.enable(False)

    # log value every 5 minutes
    sleep(2)
    loopCounter = ((loopCounter + 1) % 150)
    if loopCounter == 1:
        writeLog(rtc, ("%0.02f %0.02f" % (temperature, humidity)))

i2c.deinit()



