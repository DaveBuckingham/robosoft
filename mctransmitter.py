# MOTOR COMMAND TRANSMITTER
# DAVID BUCKINGHAM
#
# Transmittes the received motor command 4-tuple
# to a receiver on the microcontroller.

import time
import serial
import struct

class mctransmitter:

    __CONNECTION__ = None


    ##############################
    #     INITIALIZE COM         #
    ##############################

    # INITIALIZE SERIAL CONNECTION
    # CALLED AUTOMATICALLY ON FIRST CALL TO send_motor_command()
    @staticmethod
    def initialize():
        mctransmitter.__CONNECTION__ = serial.Serial(
            #port='/dev/serial/by-id/AAAAA',
            port='/dev/ttyACM0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )


    ##############################
    #          CLSOE COM         #
    ##############################

    # PROBABLY NEVER NEED TO CALL THIS
    @staticmethod
    def close():
        __CONNECTION__.close


    ##############################
    #         TRANSMIT           #
    ##############################

    # DIGITAL COMMAND
    # 2 DIGITAL PINS SO pin_index IN [0,1]
    # BINARY STATE SO value IN [True, False]
    @staticmethod
    def send_digital_command(pin_index, value):
        if (mctransmitter.__CONNECTION__ == None):
            mctransmitter.initialize()
        packed = struct.pack('!c?', 'd', pin_index, value)
        mctransmitter.__CONNECTION__.write(packed)
        return mctransmitter.__CONNECTION__.readline()

    # ANALOG COMMAND
    # 2 ANALOG PINS SO pin_index IN [0,1]
    # value IN [0, 255]
    @staticmethod
    def send_analog_command(pin_index, value):
        if (mctransmitter.__CONNECTION__ == None):
            mctransmitter.initialize()
        packed = struct.pack('!cB', 'a', pin_index, value)
        mctransmitter.__CONNECTION__.write(packed)
        return mctransmitter.__CONNECTION__.readline()

