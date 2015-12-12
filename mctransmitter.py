#
# TRANSMITS COMMANDS TO THE ARDUINO OVER SERIAL
#

import os
import sys
import time
import serial
import struct
import global_data
import record_mode


# SET TO FALSE FOR TESTING WITHOUT ARDUINO
TRANSMIT = True

# THIS WILL GET ASSIGNED DURING INITIALIZATION
CONNECTION = None


##############################
#     INITIALIZE COM         #
##############################

# INITIALIZE SERIAL CONNECTION
def initialize():
    global CONNECTION
    if (os.name == 'posix'):
        port_name = '/dev/ttyACM0'
    else:
        # TODO Sometimes COM3 sometimes COM4 depends on something I'm not sure of
        port_name = 'COM4'  

    CONNECTION = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )


##############################
#          CLOSE COM         #
##############################

# PROBABLY NEVER NEED TO CALL THIS
def close():
    CONNECTION.close


##############################
#         TRANSMIT           #
##############################

# DIGITAL TX
# 2 DIGITAL PINS SO pin_index IN [0,1]
# BINARY STATE SO value IN [True, False]
def tx_digital(pin_index, value):
    if (not isinstance(value, bool)):
        sys.exit("Non-boolean value arg to tx_digital")
    packed = struct.pack('!cB?', 'd', pin_index, value)
    if (global_data.record):
        record_mode.append_instruction(('d', pin_index, value))
    if (TRANSMIT):
        CONNECTION.write(packed)
    if (pin_index == 0):
        global_data.digital_0_sent = value
    elif (pin_index == 1):
        global_data.digital_1_sent = value

    #receive()
        

# ANALOG TX
# 2 ANALOG PINS SO pin_index IN [0,1]
# value IN [0, 255]
def tx_analog(pin_index, value):
    if (not isinstance(value, int)):
        sys.exit("Non-int value arg to tx_digital: {}".format(value))
    packed = struct.pack('!cBB', 'a', pin_index, value)
    if (global_data.record):
        record_mode.append_instruction(('a', pin_index, value))
    if (TRANSMIT):
        CONNECTION.write(packed)
    if (pin_index == 0):
        global_data.analog_0_sent = value
    elif (pin_index == 1):
        global_data.analog_1_sent = value
    #receive()


##############################
#          RECEIVE           #
##############################

# READ RESPONSE FROM ARDUINO AND
# SET VARIABLES IN global_data.py
def receive():
    print "receiving..."
    print CONNECTION.readline()

