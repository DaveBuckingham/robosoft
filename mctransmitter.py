
# MOTOR COMMAND TRANSMITTER
# DAVID BUCKINGHAM
#
# IN: (float lambda, float wavelength, bool motor_1, bool motor_2)
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

    @staticmethod
    def close():
        connection.close

    # SEND MOTOR COMMAND OVER THE WIRE
    @staticmethod
    def send_motor_command(speed, wavelength, motor_1, motor_2):
        if (mctransmitter.connection == None):
            a = 0
            #mctransmitter.initialize()

        start_flag = ':'
        ack = ':'
        packed = struct.pack('!cff??', start_flag, speed, wavelength, motor_1, motor_2)
        print packed

        #mctransmitter.connection.write(packed)
        #time.sleep(0.1)
        #line = mctransmitter.connection.readline()
        #if (line == ack):
        #    return True
        #else:
        #    return False

#TEST
mctransmitter.send_motor_command(1.2, 3.2, True, False)


