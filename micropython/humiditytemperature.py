# 
# Driver for the Adafruit HIH6130 Humidity Sensor Breakout on Micro Python PYB v1.0
#

from pyb import I2C

class HumidityTemperature(object):
    """Adafruit HIH6130 humidity sensor driver for Micro Python PYB v1.0."""

    def __init__(self, i2c, addr=0x27):
        """I2C interface and sensor device address to be used for communication"""
        self.i2c = i2c
        self.addr = addr
       
        # force refresh 
        self.hunidityValue = None
        self.temperatureValue = None
               
        if self.i2c.is_ready(self.addr):
            # start measurement
            self.i2c.send(0x00, self.addr)


    def __readValues(self):
        """Read the values from the sensor"""
        self.values = list(self.i2c.mem_read(4, self.addr, 0x00))
        self.humidityValue = ((((self.values[0] & 0x3F) << 8 ) | (self.values[1] )) / 163.83 )
        self.temperatureValue = (((((self.values[2] << 6) | (self.values[3] >> 2)) * 165) / 16383.0) - 40)


    def humidity(self):
        """Read the relative humidity (RH)"""
        if self.hunidityValue == None:
            self.__readValues()
            
        value = self.humidityValue
        self.hunidityValue = None
        return value


    def temperature(self):
        """Read the temperature in degree Celsius (°C)"""
        if self.temperatureValue == None:
            self.__readValues()
            
        value = self.temperatureValue
        self.temperatureValue = None
        return value


