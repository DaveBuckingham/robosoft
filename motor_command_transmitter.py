
# MOTOR COMMAND TRANSMITTER
# DAVID BUCKINGHAM
#
# IN: (float lambda, float wavelength, bool motor_1, bool motor_2)
# OUT: true (success) / false (failed)
# 
# DESCRIPTION:
# Transmittes the received motor command 4-tuple
# to a receiver on the microcontroller.

from time import sleep
from serial import Serial, SEVENBITS, STOPBITS_ONE, PARITY_EVEN
from  struct import pack


# CONVERT FLOATS TO BINARY FOR TRANSMISSION
# thanks to Dan Lecocq:
# http://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
def float_to_binary(num):
    packed = pack('!f', num)
    integers = [ord(c) for c in packed]
    binaries = [bin(i) for i in integers]
    stripped_binaries = [s.replace('0b', '') for s in binaries]
    padded = [s.rjust(8, '0') for s in stripped_binaries]
    return ''.join(padded)


# CONVERT BOOLS TO BINARY FOR TRANSMISSION
def bool_to_binary(val):
    if (val):
        return '00000001'
    else:
        return '00000000'
    

# THE MAIN FUNCTION
# CONVERT 4 ARGS TO BINARY AND SEND THEM OVER THE WIRE
# PRINT ANY RESPONSE (NOT SURE IF THIS IS NECESSARY)
def motor_command_transmitter(speed, wavelength, motor_1, motor_2):
    buffer = ''.join([float_to_binary(speed), float_to_binary(wavelength), bool_to_binary(motor_1), bool_to_binary(motor_2)])
    # REPLACE 'AAAAAAA' WITH SOMETHING USEFUL
    connection = Serial('/dev/serial/by-id/AAAAAA', timeout=1, baudrate=9600, bytesize=SEVENBITS, parity=PARITY_EVEN, stopbits=STOPBITS_ONE)
    connection.write(buffer)
    sleep(0.1)
    line = connection.readline()
    print line
    connection.close



