#!/usr/bin/python

__author__ = 'Jeanne-Marie and Dave'
''' Runs gamepad_interface.py as a subprocess.
Reads output from gamepad_interface.py and maps it to 4-tuples.
Calls motor_command_transmitter, passing a 4-tuple.
So four arguments to motor_command_transmitter with type:
float, float, bool, bool '''

import subprocess
import os
import sys
import threading

import record_mode
import mctransmitter  # COM WITH ARDUINO
import global_data    # SHARED WITH ui_display AND ui_map
import ui_map         # MAP BUTTON EVENTS TO PIN COMMANDS
import ui_display     # VISUAL DISPLAY

DPAD_DELAY = 1.5  # HOLD DPAD THIS LONG TO START RECORD

dpad_start_time = 0  # TRACK DPAD HOLD TIME
dpad_hold_value = 0

# record_mode_timer = threading.Timer(DPAD_DELAY, record_mode.create_record_file())

# CONVERT VALUES FROM GAMEPAD TO ARDUINO RANGES
def scale_analog(val):   # [-1,1] -> [0,255]
    return int(((val + 1) * global_data.ANALOG_MAX) / 2)

def scale_digital(val):  # [anything] -> [False, True]
    return (val > 0)


# INITIALIZE
ui_display.update()
mctransmitter.initialize()


# ITERATE OVER OUTPUT
proc = subprocess.Popen(['python', '-u', './gamepad_to_stdout.py'], stdout=subprocess.PIPE)
for line in iter(proc.stdout.readline,''):

    # REMOVE NEWLINE
    line = line.rstrip()

    # SPLIT STRING AND ASSIGN TO VARIABLES
    in_strings = line.split(" ")
    gamepad_index = int(in_strings[0])
    button_type = in_strings[1]
    button_index = int(in_strings[2])

    # DATATYPE OF VALUE DEPENDS ON BUTTON TYPE
    if (button_type == global_data.TYPE_BUTTON):
        button_value = scale_digital(int(in_strings[3]))
    elif (button_type == global_data.TYPE_AXIS):
        button_value = scale_analog(float(in_strings[3]))
    elif (button_type == global_data.TYPE_DPAD):
        button_value = (int(in_strings[3]))
    else:
        sys.exit("Read invalid button type")

    # TODO 2 sec hold down record
    # IF SELECT BUTTON PUSHED, INCREMENT MAP
    if (button_type == global_data.TYPE_BUTTON and button_index == global_data.BUTTON_SELECT and button_value):
        global_data.map_index = (global_data.map_index + 1) % len(ui_map.map_list)

    # IF DPAD, SET RECORD STATE
    elif (button_type == global_data.TYPE_DPAD):
        if button_value == 1:
            if not global_data.record:
                record_mode.initialize_record_mode(button_value)
                print "START RECORDING"
            elif global_data.record:
                record_mode.create_record_file()
                print "SAVE RECORDING"

        if button_value == 3:
            print "playback"
            record_mode.playback_from_file(1, True)

#        if (global_data.record):
#            global_data.record = 0
#            # record_mode.end_recording()
#            print "end recording"
#
#        elif ((dpad_hold_value == 0) and (button_value != 0)):
#            dpad_hold_value = button_value
#            dpad_start_time = time.time()
#        else:
#            if (button_value != 0):
#                # record_mode.load(dpad_hold_value)
#                print "load_recording " + str(dpad_hold_value)
#            dpad_hold_value = 0
#
#    print dpad_hold_value
#    if ((dpad_hold_value > 0) and (time.time() - dpad_start_time > DPAD_DELAY)):
#        # record_mode.begin_recording(dpad_hold_value)
#        print "start_recording " + str(dpad_hold_value)
#        dpad_hold_value = 0

            

    # OTHERWISE, PASS ALONG TO ui_map
    else:
        if (button_type == global_data.TYPE_AXIS):
            pass
            ui_map.map_list[global_data.map_index].update(button_type, button_index, button_value)
        elif (button_type == global_data.TYPE_BUTTON):
            pass
            ui_map.map_list[global_data.map_index].update(button_type, button_index, button_value)
        
    # REFRESH
    ui_display.update()

