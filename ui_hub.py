__author__ = 'Jeanne-Marie'
''' Runs gamepad_interface.py as a subprocess.
Reads output from gamepad_interface.py and maps it to 4-tuples.
Calls motor_command_transmitter, passing a 4-tuple.
So four arguments to motor_command_transmitter with type:
float, float, bool, bool '''

import subprocess
import os

import mctransmitter  # COM WITH ARDUINO
import global_state   # SHARED WITH ui_display AND ui_map
import ui_map         # MAP BUTTON EVENTS TO PIN COMMANDS
import ui_display     # VISUAL DISPLAY


# TODO python documentation suggests using subprocess32

# based on http://stackoverflow.com/questions/2804543/read-subprocess-stdout-line-by-line
def gamepad_to_motor_command_transmitter(whatever_would_be_input_to_gamepad_subprocess):
    proc = subprocess.Popen(['python', '-u', 'game_interface.py'], stdout=subprocess.PIPE)

   for line in iter(proc.stdout.readline,''):
        #parse line to get variables
        speed = 0
        wavelength = 0
        left = False
        right = False

        mctransmitter.send_motor_command(speed, wavelength, left, right)
