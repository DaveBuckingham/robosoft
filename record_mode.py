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
import threading

# TODO set recording limit

save_filename_prefix = 'botwurst_command_record_'
default_save_directory = 'botwurst_command_recordings'
save_file_extension = '.dat'


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
    global_data.record_start_time = datetime.datetime.now()

    make_directory(default_save_directory)
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
        #print "DIGITAL,  PIN_INDEX: ", pin_index, "VALUE: ", value
        mctransmitter.tx_digital(pin_index, value)
    elif pin_type == 'a':
        # print "ANALOG,  PIN_INDEX: ", pin_index, "VALUE: ", value
        mctransmitter.tx_analog(pin_index, value)


class Playback_From_Array(threading.Thread):
    def __init__(self, parent, queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._parent = parent
        self.start()

    def run(self):
        curr_time_stamp = 0
        for instruction in self._queue:
            while global_data.playback_paused:
                if global_data.playback_cancel:
                    break
                time.sleep(.1)
            if global_data.playback_cancel:
                break

            temp_time_stamp = instruction[3]
            time_diff = (temp_time_stamp - curr_time_stamp)
            time.sleep(time_diff)
            playback_instruction(instruction[0], instruction[1], instruction[2])

            curr_time_stamp = temp_time_stamp

        clear_playback_array()


def playback_from_file(filename, is_file_tag=False, save_directory=None):
    clear_playback_array()
    populate_playback_array_from_file(filename, is_file_tag, save_directory)
    playback_thread = Playback_From_Array(None, global_data.playback_array)
    return playback_thread


# TESTING FUNCTIONS: TO REMOVE
# class Print_Hello_Every_Sec(threading.Thread):
#     def __init__(self, parent, queue):
#         threading.Thread.__init__(self)
#         self._queue = queue
#         self._parent = parent
#         self.start()
#
#     def run(self):
#         for i in range(15):
#             print "**********HELLO THERE**************"
#             time.sleep(1)
#
# class Pause_Unpause(threading.Thread):
#     def __init__(self, parent, queue):
#         threading.Thread.__init__(self)
#         self._queue = queue
#         self._parent = parent
#         self.start()
#
#     def run(self):
#         time.sleep(2)
#         global_data.playback_paused = True
#         print "PAUSING"
#         time.sleep(5)
#         global_data.playback_cancel = True
#         print "CANCELLING"
#         time.sleep(5)
#         print "UNPAUSING"
#         global_data.playback_paused = False
#
#
# def create_dummy_instruction_file(file_tag):
#     short_delay = 0.1
#     long_delay = 1
#
#     initialize_record_mode(file_tag)
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
#     create_record_file()
#
# def main():
#     test_file_tag = 5
#     # create_dummy_instruction_file(test_file_tag)
#
#     pause_thread = Pause_Unpause(None, None)
#     playback_thread = playback_from_file(test_file_tag, True)
#     print_hello_thread = Print_Hello_Every_Sec(None, None)
#
#     print_hello_thread.join()
#     playback_thread.join()
#     pause_thread.join()
#
#     print_global_record_variables()
#
#
# main()
