# MOTOR COMMAND TRANSMITTER
# DAVID BUCKINGHAM
#
# Transmittes the received motor command 4-tuple
# to a receiver on the microcontroller.

import time
import serial
import struct

class mctransmitter:

    # SET THESE DO MODIFY BEHAVIOR
    __TEST__       = False  # GENERATE DATA TO TRANSMIT
    __DEBUG__      = False  # AFTER TRANSMIT WAIT FOR RESPONSE AND PRINT IT


    __START_FLAG__ = ":"
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

    # SEND MOTOR COMMAND OVER THE WIRE
    @staticmethod
    def send_motor_command(speed, wavelength, motor_1, motor_2):
        if (mctransmitter.__CONNECTION__ == None):
            mctransmitter.initialize()

        # CONVERTS VALUES TO C DATATYPES
        # "!" MEANS BIG ENDIAN
        # "cBB??" MEANS "char, unsigned char, unsigned char, _Bool, _Bool"
        packed = struct.pack('!cBB??', mctransmitter.__START_FLAG__, speed, wavelength, motor_1, motor_2)

        # SEND IT OUT
        mctransmitter.__CONNECTION__.write(packed)

        # CALLER MIGHT WANT THIS
        # BUT IT MEANS WAITING
        # MAKE SURE ARDUINO IS SENDING DATA
        # I.E. "#define DEBUG"
        if __DEBUG__:
            return mctransmitter.__CONNECTION__.readline()


if __TEST__:
    # TEST
    i = 1;
    while (True):
        m1 = i % 2 == 0
        m2 = i % 2 == 1
        print mctransmitter.send_motor_command(i % 256, (i + 128) % 256, m1, m2)
        i += 1

