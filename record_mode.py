"""
Provides functions for
    1) recording outputs to file
    2) replaying outputs from files
"""

import global_data
import datetime
import time

# RECORDING FUNCTIONS

def print_global_record_variable():
    print "RECORDING VARIABLE SETTINGS"
    print "===================="
    print "Recording: ", global_data.record
    print "Will store in file numbered: ", global_data.record_file_number
    print "Initial time: ", global_data.record_start_time
    print "Recording array is empty: ", (len(global_data.record_array) == 0)
    print "===================="

def initialize_record_mode(file_number):

    # if record_array is not empty back it up to file
    if global_data.record_array:
        file_tag = global_data.record_file_number + "_backup"
        create_record_file(file_tag)

    global_data.record = True
    global_data.record_file_number = file_number
    global_data.record_start_time = datetime.datetime.now()


def append_instruction(instruction):
    """
    Appends the instruction to record array in global data with time step from 0
    :param instruction: triple (PIN TYPE, PIN INDEX, VAL)
    """

    time_stamp = datetime.datetime.now()

    # TODO: look into note about datetime substraction (is exact but may overflow)
    time_diff = time_stamp - global_data.record_start_time

    pin_type = instruction[0]
    pin_index = instruction[1]
    value = instruction[2]

    record_instruction = (pin_type, pin_index, value, time_diff.total_seconds())

    global_data.record_array.append(record_instruction)


# 2) CREATE A FILE FROM RECORD ARRAY
def create_record_file(file_tag=global_data.record_file_number):
    """
    Creates a file with the list of instructions in record_array

    :param file_tag: defaults to file_number in global data, but can be overriden
    """

    # TODO: Create new file, or overwrite file if it exists
    # TODO: Copy instructions into file from record_array

    # reinitialize all variables
    global_data.record = False
    global_data.record_file_number = None
    global_data.record_start_time = None
    global_data.record_array = []


# TESTING
# def main():
#
#     short_delay = 0.1
#     long_delay = 1
#
#     initialize_record_mode(5)
#     print_global_record_variable()
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
#     print "RECORDED INSTRUCTIONS:"
#     print "===================="
#     for record_instance in global_data.record_array:
#         print record_instance
#
#     print_global_record_variable()
#     create_record_file()
#     print_global_record_variable()
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