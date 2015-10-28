
# MOTOR COMMAND TRANSMITTER
# DAVID BUCKINGHAM
#
# IN: (uint_8 lambda, uint_8 wavelength, bool motor_1, bool motor_2)
# OUT: true (success) / false (failed)
# 
# DESCRIPTION:
# Transmittes the received motor command 4-tuple
# to a receiver on the microcontroller.

import time
import serial
import struct

class mctransmitter:
    connection = None

    # INITIALIZE SERIAL CONNECTION
    # NO NEED TO CALL THIS EXPLICITELY
    # CALLED AUTOMATICALLY ON FIRST CALL TO send_motor_command()
    @staticmethod
    def initialize():
        mctransmitter.connection = serial.Serial(
            #port='/dev/serial/by-id/AAAAA',
            port='/dev/ttyUSB1',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )


    # CLOSE SERIAL CONNECTION
    # CALL THIS IF YOU'R ALL DONE COMMUNICATING
    # WE CAN PROBABLY SKIP CALLING THIS
    @staticmethod
    def close():
        connection.close


    # SEND MOTOR COMMAND OVER THE WIRE
    @staticmethod
    def send_motor_command(speed, wavelength, motor_1, motor_2):
        if (mctransmitter.connection == None):
            mctransmitter.initialize()

        start_flag = ':'
        ack = ':'
        packed = struct.pack('!cBB??', start_flag, speed, wavelength, motor_1, motor_2)

        mctransmitter.connection.write(packed)
        time.sleep(0.1)

        # WE PROBABLY DONT NEED TO USE ACKS
        #line = mctransmitter.connection.readline()
        #if (line == ack):
        #    return True
        #else:
        #    return False

#TEST
#mctransmitter.send_motor_command(74, 212, True, False)


