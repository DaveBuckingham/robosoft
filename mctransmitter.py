#
# TRANSMITS COMMANDS TO THE ARDUINO OVER SERIAL
#

import sys
import time
import serial
import struct
import global_data


# SET TO FALSE FOR TESTING WITHOUT ARDUINO
TRANSMIT = True

# WAIT FOR RESPONSE AFTER EACH TX
RECEIVE = False

# THIS WILL GET ASSIGNED DURING INITIALIZATION
CONNECTION = None


##############################
#     INITIALIZE COM         #
##############################

# INITIALIZE SERIAL CONNECTION
# CALLED AUTOMATICALLY ON FIRST
# CALL TO tx_digital() or tx_analog()
def initialize():
    global CONNECTION
    CONNECTION = serial.Serial(
        # WHAT SHOULD THIS BE FOR WINDOWS? MAC?
        # SHOULD DETECT OS AND ASSIGNN THIS ACCORDINGLY
        port='/dev/ttyACM0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    return CONNECTION.readline()


##############################
#          CLSOE COM         #
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

#def receive():
#    if (RECEIVE):
#        CONNECTION.readline()


