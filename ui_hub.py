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
import time
import gamepad_reader

MAIN_LOOP_DELAY = 0.01
DISPLAY_UPDATE_DELAY = 5

# CONVERT VALUES FROM GAMEPAD TO ARDUINO RANGES
def scale_analog(val):   # [-1,1] -> [0,255]
    return int(((val + 1) * global_data.ANALOG_MAX) / 2)

def scale_digital(val):  # [anything] -> [False, True]
    return (val > 0)

playback_timer = None

# ============== VARIABLES AND FUNCTIONS FOR DPAD USE IN RECORD MODE =========================
dpad_press_timer = None # DPAD TIMER TRIGGERS RECORD MODE AFTER TIME SPECIFIED BY DPAD DELAY
DPAD_DELAY = 1  # HOLD DPAD THIS LONG TO START RECORDING


silence_dpad = False    # DPAD NOISE MANAGEMENT (Ignore diagonal presses of dpad)
SILENCE_INTERVAL = 1    # DPAD WILL IGNORE SIGNALS FOR THIS LONG AFTER DIAGONAL IS PRESSED

dpad_released = True

def unsilence_dpad():
    global silence_dpad
    silence_dpad = False


def execute_dpad(button_value):
    global dpad_released
    global dpad_press_timer
    # IF OFF-AXIS: IGNORE DPAD BUTTON PRESSES FOR "SILENCE_INTERVAL"
    global silence_dpad

    if button_value == -1:
        silence_dpad = True
        threading.Timer(SILENCE_INTERVAL, unsilence_dpad).start()

    else:
        # DPAD WAS PRESSED
        if button_value != 0 and not silence_dpad:
            if not global_data.playback:
                if not global_data.record:
                    record_mode.playback_file_tag = button_value
                    dpad_press_timer = threading.Timer(DPAD_DELAY, record_mode.initialize_record_mode, [button_value])
                    dpad_press_timer.start()
                    dpad_released = False

                elif dpad_released:
                    record_mode.create_record_file()
            else:
                record_mode.stop_playback()

        # DPAD WAS RELEASED
        if button_value == 0:
            if dpad_press_timer:
                if dpad_press_timer.is_alive():
                    global_data.record = False
                    dpad_press_timer.cancel()
                    dpad_press_timer.join()

                    record_mode.playback_from_file(record_mode.playback_file_tag, True)

            dpad_released = True


def process_gamepad_output(line):

    transmitted_values = None   # If an instruction was transmitted using mctransmitter:
                                #   "transmitted_values" will be a dictionary representing
                                #   the values sent to mctransmitter,  where the keys are:
                                #   'Signal_Type', 'Pin_Index' and 'TX_Value'

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
        button_value = int(in_strings[3])
    else:
        sys.exit("Read invalid button type")


    # IF SELECT BUTTON PUSHED, INCREMENT MAP
    if (button_type == global_data.TYPE_BUTTON and button_index == global_data.BUTTON_SELECT and button_value):
        global_data.map_index = (global_data.map_index + 1) % len(ui_map.map_list)

    # DPAD: Used for record mode functions
    elif (button_type == global_data.TYPE_DPAD):
        execute_dpad(button_value)

    # OTHERWISE, PASS ALONG TO ui_map
    else:
        to_send = ui_map.map_list[global_data.map_index].update(button_type, button_index, button_value)

        if to_send is not None:
            transmitted_values = to_send

            if to_send['Signal_Type'] == 'a':
                mctransmitter.tx_analog(to_send['Pin_Index'], to_send['TX_Value'])
            if to_send['Signal_Type'] == 'd':
                mctransmitter.tx_digital(to_send['Pin_Index'], to_send['TX_Value'])

    return transmitted_values


def playback():
    global playback_timer

    # Check: there is no instruction waiting to be played back
    if playback_timer is None or not playback_timer.is_alive():
        # Finished playing all the instructions in the playback array

        # Playback next instruction in playback array after delay specified in stored instruction
        # Indices correspond to: 0: analog/digital
        #                        1: pin index
        #                        2: value
        #                        3: timestamp (interval between last and current instruction)

        playback_instruction = global_data.playback_array.pop()
        playback_timer = threading.Timer(playback_instruction[3],
                                         record_mode.playback_instruction, (playback_instruction[0],
                                                                            playback_instruction[1],
                                                                            playback_instruction[2]))
        playback_timer.start()

        if not global_data.playback_array:
            record_mode.populate_playback_array_from_file(record_mode.playback_file_tag, True)
def main():
    # INITIALIZE
    display_update_counter = 0
    ui_display.update()

    gamepad_reader.initialize_gamepad_reader()

    if mctransmitter.TRANSMIT:
        mctransmitter.initialize()

    # MAIN LOOP: Will run as long as program is running
    while True:
        time.sleep(MAIN_LOOP_DELAY)

        # Check if there is any input from gamepad
        gamepad_reader.read_gamepad()

        # If there is input from gamepad, process it accordingly
        if global_data.last_input_from_gamepad is not None:
            transmitted_from_gamepad = process_gamepad_output(global_data.last_input_from_gamepad)
            global_data.last_input_from_gamepad = None

            if global_data.record and transmitted_from_gamepad is not None:
                record_mode.append_instruction((transmitted_from_gamepad['Signal_Type'],
                                                transmitted_from_gamepad['Pin_Index'],
                                                transmitted_from_gamepad['TX_Value']))

        # Check for playback
        if global_data.playback:
            playback()

        # Refresh display after interval: DISPLAY_UPDATE_DELAY
        if display_update_counter == DISPLAY_UPDATE_DELAY:
            ui_display.update()
            display_update_counter = 0

        display_update_counter += 1

main()
