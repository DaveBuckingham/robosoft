"""
Provides functions for
    1) recording outputs to file
    2) replaying outputs from files
"""

import global_data
import datetime
import os
import errno


# HELPER FUNCTIONS FOR DIRECTORY NAVIGATION
def get_curr_directory():
    curr_dir = os.getcwd()
    curr_dir = os.path.split(curr_dir)[1]

    return curr_dir


def is_current_directory(directory_name):
    curr_dir = get_curr_directory()

    return curr_dir == directory_name


def make_directory(directory_name):
    try:
        os.makedirs(directory_name + '/')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def change_to_directory(directory_name):
    changed_dir = False

    if not is_current_directory(directory_name):
        try:
            os.chdir(directory_name + '/')
        except OSError:
            try:
                os.chdir('../' + directory_name + '/')
            except OSError:
                print "***ERROR WHILE CHANGING TO DIRECTORY: ", directory_name, " is missing, creating new directory***"
                os.makedirs(directory_name + '/')
                os.chdir(directory_name + '/')

        changed_dir = True

    return changed_dir


# HELPER FUNCTION FOR LOOKING AT GLOBAL VARIABLES
def print_global_record_variables():
    print "RECORDING VARIABLE SETTINGS"
    print "===================="
    print "Recording: ", global_data.record
    print "Will store in file numbered: ", global_data.record_file_number, " in directory: ", global_data.record_save_directory
    print "Initial time: ", global_data.record_start_time
    print "Recording array is empty: ", (len(global_data.record_array) == 0)
    print "===================="


# RECORDING FUNCTIONS
def initialize_record_mode(file_number, save_directory=None):
    """
    Sets all the global_data variables to reflect that we are now recording
    Creates the specified directory in which the recording file is to be saved, if directory does not exist

    :param file_number: Tag for file where recording will be stored
    :param save_directory: Directory in which we want to save recording
                    - when save_directory is not specified, defaults to the directory in global data
    """

    if save_directory is None:
        save_directory = global_data.record_save_directory

    # if record_array is not empty back it up to file
    if global_data.record_array:
        file_tag = global_data.record_file_number + "_backup"
        create_record_file(file_tag)

    global_data.record = True
    global_data.record_file_number = file_number
    global_data.record_save_directory = save_directory
    global_data.record_start_time = datetime.datetime.now()

    if not is_current_directory(save_directory):
        make_directory(save_directory)


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
def create_record_file(file_tag=None):
    """
    Creates a file with the list of instructions in record_array
    :param file_tag: defaults to file_number in global data
    """

    if file_tag is None:
        file_tag = global_data.record_file_number

    # Remember the directory we were in before changing into save_directory
    #   note: the change_to_directory function makes it so that once we have
    #         changed into save_directory, the previous directory was either:
    #               1) the save_directory itself
    #               2) a parent of save_directory
    #               3) a sibling of save_directory
    curr_dir = get_curr_directory()

    # changed_dir is true if previous directory was not save directory
    changed_dir = change_to_directory(global_data.record_save_directory)

    record_filename = 'botwurst_command_record_' + str(file_tag) + '.txt'

    # Create new file, or overwrite file if it exists
    with open(record_filename, 'w') as recording_file:
        # Copy all commands to the file
        for command in global_data.record_array:
            recording_file.write(str(command) + '\n')

    # Return to previous working directory
    if changed_dir:
        os.chdir('../')
    if not is_current_directory(curr_dir):
        os.chdir(curr_dir + '/')

    # Reinitialize all record variables
    global_data.record = False
    global_data.record_file_number = None
    global_data.record_start_time = None
    global_data.record_array = []

# TODO: PLAYBACK FUNCTIONS
    
# TESTING
# def main():
#
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
#     print_global_record_variables()
#     print "We are in save directory:", is_current_directory(global_data.record_save_directory)
#     create_record_file()
#     print "We are in save directory:", is_current_directory(global_data.record_save_directory)
#     print os.getcwd()
#     print_global_record_variables()
#
#
# main()

# TO TEST TIME STAMP CREATION PUT IN MAIN
#
#     time_stamp_list = []
#     time_stamp = datetime.datetime.now()
#
#     time_stamp_list.append(time_stamp)
#
#     for i in range(9):
#
#         time.sleep(.1)
#         temp_time = datetime.datetime.now()
#         time_stamp_list.append(temp_time)
#
#     print time_stamp_list
#
#     for time_stamp_item in time_stamp_list:
#
#         time_diff = time_stamp_item - time_stamp
#         print time_diff.total_seconds()
#