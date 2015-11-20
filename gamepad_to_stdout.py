'''
GAMEPAD INTERFACE
Ethan Laverack and David Buckingham

Description: Uses PyGame joystick library to pull data off of gamepad and send axis
             and button states to ui_hub through standard out

FOR REFERENCE: https://www.pygame.org/docs/ref/joystick.html

CONSULT global_data.py FOR DEFINITIONS -db

'''

import pygame
import sys
import time


AXIS_ZERO_THRESHOLD = 0.13
AXIS_TIME_THRESHOLD = .15


################
#  INITIALIZE  #
################
pygame.init()
pygame.joystick.init()
gamepad_count = pygame.joystick.get_count()
if gamepad_count:
    for i in range(gamepad_count):
        gamepad = pygame.joystick.Joystick(i)
        gamepad.init()
else:
    sys.exit("no gamepad")

last_axis_time = [0.0] * 6
last_axis_value = [0.0] * 6
new_axis_value = [0.0] * 6

################
# CONVERT DPAD #
################
def dpad_convert(input):
    if (input == (-1, 0)):
        return 1
    elif (input == (0, 1)):
        return 2
    elif (input == (1, 0)):
        return 3
    elif (input == (0, -1)):
        return 4
    return 0



################
#     LOOP     #
################
while gamepad_count:
    for event in pygame.event.get():

        # BUTTONS
        if event.type == pygame.JOYBUTTONDOWN:
            print '{} b {} {}'.format(event.joy, event.button, 1)
        if event.type == pygame.JOYBUTTONUP:
            print '{} b {} {}'.format(event.joy, event.button, 0)

        # AXES
        if event.type == pygame.JOYAXISMOTION:
                if (abs(event.value) < AXIS_ZERO_THRESHOLD):
                    new_axis_value[event.axis] = 0.0
                elif (event.value + 1 < AXIS_ZERO_THRESHOLD):
                    new_axis_value[event.axis] = -1.0
                elif (event.value - 1 > -AXIS_ZERO_THRESHOLD):
                    new_axis_value[event.axis] = 1.0
                else:
                    new_axis_value[event.axis] = event.value

        # DPAD
        if event.type == pygame.JOYHATMOTION:
            print '{} d {} {}'.format(event.joy, event.hat, dpad_convert(event.value))


    now = time.time()
    for i in range(0, 6):
        if (new_axis_value[i] != last_axis_value[i]):
            if ((now - last_axis_time[i]) > AXIS_TIME_THRESHOLD):
                last_axis_time[i] = now
                last_axis_value[i] = new_axis_value[i]
                print '{} a {} {}'.format(0, i, last_axis_value[i])


pygame.quit()
