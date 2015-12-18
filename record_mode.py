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


playback_file_tag = None

save_filename_prefix = 'botwurst_command_record_'
default_save_directory = 'botwurst_command_recordings'
save_file_extension = '.dat'

prev_time_stamp = None


# TODO set recording limit]
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
    print "Will store in file numbered: ", global_data.record_file_number, " in directory: ", default_save_directory
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
    global prev_time_stamp
    prev_time_stamp = datetime.datetime.now()

    # if save_directory already exists as subdirectory, nothing will happen
    make_directory(default_save_directory)


def append_instruction(instruction):
    """
    Appends the instruction to record array in global data with time step from 0
    :param instruction: triple (PIN TYPE, PIN INDEX, VAL)
    """
    global prev_time_stamp
    time_stamp = datetime.datetime.now()

    # TODO: look into note about datetime subtraction (is exact but may overflow)
    time_diff = time_stamp - prev_time_stamp
    prev_time_stamp = time_stamp

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
        save_directory = default_save_directory

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


# 2) PLAYBACK FUNCTIONS
def clear_playback_array():
    global_data.playback_array = []


def stop_playback():
    global_data.playback = False
    clear_playback_array()


def populate_playback_array_from_file(filename, is_file_tag=False, save_directory=None):
    """
    Appends instructions from current file to playback array

    :param filename: name of file containing recording information
    :param is_file_tag: True if only using number to identify file (default False)
    :param save_directory: default directory specified in global data
    """
    if save_directory is None:
        save_directory = default_save_directory

    if is_file_tag:
        filename = save_filename_prefix + str(filename)

    playback_file = open(save_directory + '/' + str(filename) + save_file_extension, 'r')
    playback_file_lines = playback_file.readlines()

    for line in playback_file_lines:
        global_data.playback_array.append((eval(line.rstrip())))


def playback_instruction(pin_type, pin_index, value):
    if pin_type == 'd':
        # print "DIGITAL,  PIN_INDEX: ", pin_index, "VALUE: ", value
        mctransmitter.tx_digital(pin_index, value)
    elif pin_type == 'a':
        # print "ANALOG,  PIN_INDEX: ", pin_index, "VALUE: ", value
        mctransmitter.tx_analog(pin_index, value)




def playback_from_file(filename, is_file_tag=False, save_directory=None):
    clear_playback_array()
    populate_playback_array_from_file(filename, is_file_tag, save_directory)
    global_data.playback = True
    global_data.playback_file_number = filename

