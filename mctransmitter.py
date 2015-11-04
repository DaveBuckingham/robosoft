# MOTOR COMMAND TRANSMITTER
# DAVID BUCKINGHAM
#
# Transmittes the received motor command 4-tuple
# to a receiver on the microcontroller.

import time
import serial
import struct


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
        #port='/dev/serial/by-id/AAAAA',
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

# DIGITAL COMMAND
# 2 DIGITAL PINS SO pin_index IN [0,1]
# BINARY STATE SO value IN [True, False]
def tx_digital(pin_index, value):
    if (CONNECTION == None):
        initialize()
    packed = struct.pack('!cB?', 'd', pin_index, value)
    CONNECTION.write(packed)
    return CONNECTION.readline()

# ANALOG COMMAND
# 2 ANALOG PINS SO pin_index IN [0,1]
# value IN [0, 255]
def tx_analog(pin_index, value):
    if (CONNECTION == None):
        initialize()
    packed = struct.pack('!cBB', 'a', pin_index, value)
    CONNECTION.write(packed)
    return CONNECTION.readline()


