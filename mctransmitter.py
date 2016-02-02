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

TRANSMIT_DELAY = 0.08  # SECONDS

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

    if (TRANSMIT):
        if (os.name == 'posix'):
            port_name = '/dev/ttyACM0'
        else:
            port_name = 'COM4'  

        CONNECTION = serial.Serial(
            port=port_name,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0   # don't block when reading
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


# GAIT TX
def tx_gait(event_list):
    packed = struct.pack('!c', 't')
    if (TRANSMIT):
        CONNECTION.write(packed)
    for event in event_list:
        time.sleep(TRANSMIT_DELAY)
        packed = struct.pack('!LBBBB', event['activation_time'], event['motor_index'], event['direction'], event['pwm'], event['skip'])
        if (TRANSMIT):
            CONNECTION.write(packed)
            #print CONNECTION.readline()

#def tx_reset():
#    packed = struct.pack('!c', 'r')
#    if (TRANSMIT):
#        CONNECTION.write(packed)



##############################
#          RECEIVE           #
##############################

# READ RESPONSE FROM ARDUINO AND
# SET VARIABLES IN global_data.py
def receive():
    line = CONNECTION.readline()
    if (len(line) > 0):
        sys.stdout.write(line);
        #print line;

