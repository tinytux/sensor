#
# Driver for the Adafruit 7-segment LED HT16K33 backpack on Micro Python PYB v1.0
#

from pyb import I2C
from time import sleep

charMap = {
    ' ' : 0x00,
    '0' : 0x3F,
    '1' : 0x06,
    '2' : 0x5B,
    '3' : 0x4F,
    '4' : 0x66,
    '5' : 0x6D,
    '6' : 0x7D,
    '7' : 0x07,
    '8' : 0x7F,
    '9' : 0x6F,
    'A' : 0x77,
    'B' : 0x7C,
    'C' : 0x39,
    'D' : 0x5E,
    'E' : 0x79,
    'F' : 0x71
} 

digitOffset = {
    0   : 0,
    1   : 2,
    2   : 6,
    3   : 8
} 


class SevenSegment(object):
    """Adafruit 7 segment LED backpack driver for Micro Python PYB v1.0."""

    def __init__(self, i2c, addr=0x70):
        """I2C interface and 7 segment device address to be used for communication"""
        self.i2c = i2c
        self.addr = addr
        self.displaymode = 0x81    # blink off, display on
        
        if self.i2c.is_ready(self.addr):
            # turn clock on
            self.i2c.send(0x21, self.addr)
            sleep(0.2)
            # set brightness
            self.i2c.send(0xE2, self.addr)
            #self.i2c.send(0xA0, self.addr)
            sleep(0.2)        
            # default: blink off, display on
            self.blink(False)
            self.enable(True)


    def enable(self, on = True):
        """Switch display on/off."""
        if on:
            self.displaymode = self.displaymode | 0x01
        else:
            self.displaymode = self.displaymode & 0xFE
        
        self.i2c.send(self.displaymode, self.addr)


    def blink(self, blink = False):
        """Set blinking on/off."""
        if blink:
            self.displaymode = self.displaymode | 0x04
        else:
            self.displaymode = self.displaymode & 0xFB

        self.i2c.send(self.displaymode, self.addr)


    def write(self, text):
        """Display a text. Format is 'nn[.:]nn'"""            
        self.i2c.mem_write(self.__buildBuffer(text), self.addr, 0x00)


    def __buildBuffer(self, text):
        """Build a buffer containing the given text"""
        buf = [0x39, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        dotPos = (text.find('.') - 1)
        text = text.replace('.', '')
        text = text.replace('-', '')
        for i, c in enumerate(text):
            value = charMap[text[i]]
            if i == dotPos:
                value = (value | 0x80)
            buf[digitOffset[i]] = value
        return bytearray(buf)


