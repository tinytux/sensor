# boot.py -- runs on boot-up

import pyb

pyb.LED(3).on()                 # indicate we are waiting for switch press
pyb.delay(2000)                 # wait for user to maybe press the switch
switch_value = pyb.Switch()()   # sample the switch at end of delay
pyb.LED(3).off()                # indicate that we finished waiting for the switch

pyb.LED(4).on()                 # indicate that we are selecting the mode

if switch_value:
    # button pressed, mount SD card as usb storage
    pyb.usb_mode('CDC+MSC')
    pyb.main('debug.py')
else:
    # no button pressed, SD card can be used by script
    pyb.usb_mode('CDC+HID')
    pyb.main('displaytemp.py')

pyb.LED(4).off()                # indicate that we finished selecting the mode


