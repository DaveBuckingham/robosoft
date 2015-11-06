#!/usr/bin/python


__author__ = 'Jeanne-Marie'
''' Runs gamepad_interface.py as a subprocess.
Reads output from gamepad_interface.py and maps it to 4-tuples.
Calls motor_command_transmitter, passing a 4-tuple.
So four arguments to motor_command_transmitter with type:
float, float, bool, bool '''

import subprocess
import os

import mctransmitter  # COM WITH ARDUINO
import global_data    # SHARED WITH ui_display AND ui_map
import ui_map         # MAP BUTTON EVENTS TO PIN COMMANDS
import ui_display     # VISUAL DISPLAY


# PASS BUTTON VALUES THROUGH THESE
# BEFORE SENDING THEM TO MAP
def scale_analog(val):   # [-1,1] -> [0,255]
    return (((val + 1) * ANALOG_MAX) / 2)

def scale_digital(val):  # [anything] -> [False, True]
    return (val > 0)




ui_display.update()


# based on http://stackoverflow.com/questions/2804543/read-subprocess-stdout-line-by-line

proc = subprocess.Popen(['python', '-u', './gamepad_interface.py'], stdout=subprocess.PIPE)
for line in iter(proc.stdout.readline,''):
    line = line.rstrip()  # REMOVE NEWLINE
    strings = line.split(" ")
    gamepad_index = int(strings[0])
    button = strings[1]
    value = int(strings[0])


    if (button == global_data.BUTTON_SELECT and value == True):
        global_data.map_index = (global_data.map_index + 1) % len(ui_map.map_list)
    else:
        ui_map.map_list[global_data.map_index].update(button, value)

    ui_display.update()

