"""
Provides functions for
    1) recording outputs to file
    2) replaying outputs from files
"""

import global_data
import mctransmitter
import datetime
import os
import errno
import time

save_filename_prefix = 'botwurst_command_record_'
record_save_directory = 'botwurst_command_recordings'
save_file_extension = '.dat'


# TODO: look at threading so that we could run multiple processes at once.
#       - eg. record over playback, or pause a playback


def make_directory(directory_name):
    try:
        os.makedirs(directory_name + '/')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def set_default_save_directory(directory_name):
    record_save_directory = directory_name


# HELPER FUNCTION FOR LOOKING AT GLOBAL VARIABLES
def print_global_record_variables():
    print "RECORDING VARIABLE SETTINGS"
    print "===================="
    print "Recording: ", global_data.record
    print "Will store in file numbered: ", global_data.record_file_number, " in directory: ", record_save_directory
    print "Initial time: ", global_data.record_start_time
    print "Recording array is empty: ", (len(global_data.record_array) == 0)
    print "===================="


# RECORDING FUNCTIONS
def initialize_record_mode(file_number):
    """
    Sets all the global_data variables to reflect that we are now recording
    Creates the specified directory in which the recording file is to be saved, if directory does not exist

    :param file_number: Tag for file where recording will be stored
    """

    # if record_array is not empty back it up to file
    if global_data.record_array:
        file_tag = global_data.record_file_number + "_backup"
        create_record_file(file_tag)

    global_data.record = True
    global_data.record_file_number = file_number
    global_data.record_start_time = datetime.datetime.now()

    make_directory(record_save_directory)
    # if save_directory already exists as subdirectory, nothing will happen


def append_instruction(instruction):
    """
    Appends the instruction to record array in global data with time step from 0
    :param instruction: triple (PIN TYPE, PIN INDEX, VAL)
    """

    time_stamp = datetime.datetime.now()

    # TODO: look into note about datetime subtraction (is exact but may overflow)
    time_diff = time_stamp - global_data.record_start_time

    pin_type = instruction[0]
    pin_index = instruction[1]
    value = instruction[2]

    record_instruction = (pin_type, pin_index, value, time_diff.total_seconds())

    global_data.record_array.append(record_instruction)


# 2) CREATE A FILE FROM RECORD ARRAY
def create_record_file(file_tag=None, save_directory=None):
    """
    Creates a file with the list of instructions in record_array
    :param file_tag: defaults to file_number in global data
    """

    if file_tag is None:
        file_tag = global_data.record_file_number
    if save_directory is None:
        save_directory = record_save_directory

    record_filename = save_directory + '/' + save_filename_prefix + str(file_tag) + save_file_extension

    # Create new file, or overwrite file if it exists
    with open(record_filename, 'w') as recording_file:
        # Copy all commands to the file
        for command in global_data.record_array:
            recording_file.write(str(command) + '\n')

    # Reinitialize all record variables
    global_data.record = False
    global_data.record_file_number = None
    global_data.record_start_time = None
    global_data.record_array = []


# TODO: PLAYBACK FUNCTIONS
def clear_playback_array():
    global_data.playback_array = []


def populate_playback_array_from_file(filename, is_file_tag=False, save_directory=None):
    """
    Appends instructions from current file to playback array

    :param filename: name of file containing recording information
    :param is_file_tag: True if only using number to identify file (default False)
    :param save_directory: default directory specified in global data
    """
    if save_directory is None:
        save_directory = record_save_directory

    if is_file_tag:
        filename = save_filename_prefix + str(filename)

    playback_file = open(save_directory + '/' + str(filename) + save_file_extension, 'r')
    playback_file_lines = playback_file.readlines()

    for line in playback_file_lines:
        global_data.playback_array.append((eval(line.rstrip())))


def playback_instruction(instruction_from_array):
    if instruction_from_array[0] == 'd':
        print "DIGITAL,  PIN_INDEX: ", instruction_from_array[1], "VALUE: ", instruction_from_array[2]
        # mctransmitter.tx_digital(instruction_from_array[1], instruction_from_array[2])
    elif instruction_from_array[0] == 'a':
        print "ANALOG,  PIN_INDEX: ", instruction_from_array[1], "VALUE: ", instruction_from_array[2]
        # mctransmitter.tx_analog(instruction_from_array[1], instruction_from_array[2])


def playback_from_array():
    curr_time_stamp = 0
    for instruction in global_data.playback_array:
        # TODO: I think that this won't work at the moment, because we can't pause while this process is happening?
        # while global_data.playback_paused:
        #     time.sleep(.5)
        #     print "PLAYBACK PAUSED"

        temp_time_stamp = instruction[3]
        time_diff = (temp_time_stamp - curr_time_stamp)
        time.sleep(time_diff)
        playback_instruction(instruction)

        curr_time_stamp = temp_time_stamp

    clear_playback_array()


def playback_from_file(filename, is_file_tag=False, save_directory=None):
    clear_playback_array()
    populate_playback_array_from_file(filename, is_file_tag, save_directory)
    playback_from_array()


# TESTING
# def main():
#     print "***** FIRST LINE IN MAIN ***************"
#     print "****************************************"
#     short_delay = 0.1
#     long_delay = 1
#
#     initialize_record_mode(5)
#     print_global_record_variables()
#
#     i = 1
#     j = 0
#
#     for iterator in range(10):
#         i_is_even = (1 == i%2)
#
#         digital_instruction = ('d', 0, i_is_even)
#         append_instruction(digital_instruction)
#
#         time.sleep(short_delay)
#
#         digital_instruction = ('d', 1, not i_is_even)
#         append_instruction(digital_instruction)
#
#         time.sleep(short_delay)
#
#         val = abs((j % 510) - 255)
#
#         analog_instruction = ('a', 0, val)
#         append_instruction(analog_instruction)
#
#         time.sleep(short_delay)
#
#         analog_instruction = ('a', 1, 255 - val)
#         append_instruction(analog_instruction)
#
#         time.sleep(long_delay)
#
#         i = i + 1
#         j = j + 20
#
#     # print "RECORDED INSTRUCTIONS:"
#     # print "===================="
#     # for record_instance in global_data.record_array:
#     #     print record_instance
#
#     create_record_file()
#     playback_from_file(5, True)
#     print_global_record_variables()
#
# main()
