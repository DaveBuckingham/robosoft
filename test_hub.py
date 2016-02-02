#!/usr/bin/python

# BY DAVE, FOR TESTING GAITS

import time
import subprocess
import os
import sys
import pygame


import mctransmitter  # COM WITH ARDUINO


EXPAND = 0
CONTRACT = 1

NUM_MOTORS = 3

# FOR UI
current_motor = 0
highlighted_variable = 0

# FOR MANUAL MOTOR CONTROL
motorstate = [0, 0, 0]   # 0->stopped   1->expanding    2->contracting

# TOGGLED WITH THE <TAB> KEY
CONTROL_MANUAL = 0
CONTROL_TRANSMIT = 1
CONTROL_WALK = 2
control_mode = CONTROL_MANUAL

# ROBOT MOVING?
WALK_RESET = 0
WALK_PAUSE = 1
WALK_PLAY = 2
walk_mode = WALK_RESET

input_state = False   # ENTERING A VARIABLE
input_value = 0       # VARIABLE VALUE BEING ENTERED

frame = 0  # COUNTER FOR ANIMATION

KEY_UP       = 273
KEY_DOWN     = 274
KEY_RIGHT    = 275
KEY_LEFT     = 276
KEY_TAB      = 9
KEY_RETURN   = 13 
KEY_SPACE    = 32
KEY_TRANSFER = 116  # 't'
KEY_QUIT     = 113  # 'q'

HIGHLIGHT = (255, 255, 0)
WHITE = (200, 200, 255)

ANIMATION = [ \
             "------------------------", \
             "-----------------------.", \
             "----------------------,.", \
             "---------------------.,.", \
             "---------------------.,.", \
             "-------------------'-.,.", \
             "------------------`'-.,.", \
             "-----------------'`'-.,.", \
             "-----------------'`'-.,.", \
             "---------------.-'`'-.,.", \
             "--------------,.-'`'-.,.", \
             "-------------.,.-'`'-.,.", \
             "-------------.,.-'`'-.,.", \
             "-----------'-.,.-'`'-.,.", \
             "----------`'-.,.-'`'-.,.", \
             "---------'`'-.,.-'`'-.,.", \
             "---------'`'-.,.-'`'-.,.", \
             "-------.-'`'-.,.-'`'-.,.", \
             "------,.-'`'-.,.-'`'-.,.", \
             "-----.,.-'`'-.,.-'`'-.,.", \
             "-----.,.-'`'-.,.-'`'-.,.", \
             "---'-.,.-'`'-.,.-'`'-.,.", \
             "--`'-.,.-'`'-.,.-'`'-.,.", \
             "-'`'-.,.-'`'-.,.-'`'-.,.", \
             "'`'-.,.-'`'-.,.-'`'-.,.-", \
             "`'-.,.-'`'-.,.-'`'-.,.-'", \
             "'-.,.-'`'-.,.-'`'-.,.-'`", \
             "-.,.-'`'-.,.-'`'-.,.-'`'", \
             ".,.-'`'-.,.-'`'-.,.-'`'-", \
             ",.-'`'-.,.-'`'-.,.-'`'-.", \
             ".-'`'-.,.-'`'-.,.-'`'-.,", \
]
ANIMATION_CONTINUE = 23

animation_frame = 0

variable_names = [
    'expanded_delay',
    'contract_time',
    'contracted_delay',
    'expand_time',
    'contract_speed',
    'expand_speed',
    'motor_1_offset',
    'motor_2_offset'
]

VARIABLE_MAXS = [60000, 60000, 60000, 60000, 255, 255, 60000, 60000]

variables = {
    variable_names[0]: 6000,
    variable_names[1]: 6000,
    variable_names[2]: 6000,
    variable_names[3]: 6000,
    variable_names[4]: 150,
    variable_names[5]: 150,
    variable_names[6]: 2000,
    variable_names[7]: 4000,
}



def transfer():
    event_list = []
    cycle_length = variables['expanded_delay'] +  \
                   variables['contract_time'] + \
                   variables['contracted_delay'] + \
                   variables['expand_time']


    for i in range(0, NUM_MOTORS):
        activation_time = 0
        skip = 0
        if (i == 1):
            activation_time = variables['motor_1_offset']
        elif (i == 2):
            activation_time = variables['motor_2_offset']

        # START CONTRACTING
        activation_time = (activation_time + variables['expanded_delay'])
        if (activation_time >= cycle_length):
            activation_time = activation_time % cycle_length
            skip = 1
        event_list.append({
            'activation_time': activation_time,
            'motor_index': i,
            'direction': CONTRACT,
            'pwm':variables['contract_speed'],
            'skip': skip,
        })

        # STOP CONTRACTING
        activation_time = (activation_time + variables['contract_time'])
        if (activation_time >= cycle_length):
            activation_time = activation_time % cycle_length
            skip = 1
        event_list.append({
            'activation_time': activation_time,
            'motor_index': i,
            'direction': CONTRACT,
            'pwm': 0,
            'skip': skip,
        })

        # START EXPANDING
        activation_time = (activation_time + variables['contracted_delay'])
        if (activation_time >= cycle_length):
            activation_time = activation_time % cycle_length
            skip = 1
        event_list.append({
            'activation_time': activation_time,
            'motor_index': i,
            'direction': EXPAND,
            'pwm': variables['expand_speed'],
            'skip': skip,
        })

        # STOP EXPANDING
        activation_time = (activation_time + variables['expand_time'])
        if (activation_time >= cycle_length):
            activation_time = activation_time % cycle_length
            skip = 1
        event_list.append({
            'activation_time': activation_time,
            'motor_index': i,
            'direction': EXPAND,
            'pwm': 0,
            'skip': skip,
        })

     # SORT
    event_list = sorted(event_list, key=lambda k: k['activation_time']) 

    mctransmitter.tx_gait(event_list)

    print "transmitting gait"
    for event in event_list:
        print "time: " + str(event['activation_time']),
        print "motor: " + str(event['motor_index']),
        print "dir: " + str(event['direction']),
        print "pwm: " + str(event['pwm']),
        print "skip: " + str(event['skip'])




def refresh():
    screen.fill((0,0,0))
    colors = [WHITE] * NUM_MOTORS
    if (control_mode == CONTROL_MANUAL):
        colors[current_motor] = HIGHLIGHT

    for i in range(0, NUM_MOTORS):
        message = ""
        if (motorstate[i] == 1):
            message += ">>> "
        elif (motorstate[i] == 2):
            message += "<<< "
        else:
            message += "    "
        message += "motor " + str(i)
        if (motorstate[i] == 1):
            message += " <<<"
        elif (motorstate[i] == 2):
            message += " >>>"
        label = myfont.render(message, 1, colors[i])
        screen.blit(label, (0, i * 15))


    colors = [WHITE] * len(variables)
    if (control_mode == CONTROL_TRANSMIT):
        colors[highlighted_variable] = HIGHLIGHT
    for i in range(0, len(variables)):
        label = myfont.render(variable_names[i], 1, colors[i])
        screen.blit(label, (200, i * 15))
        if (input_state and i == highlighted_variable):
            label = myfont.render("= " + str(input_value), 1, colors[i])
        else:
            label = myfont.render("= " + str(variables[variable_names[i]]), 1, colors[i])
        screen.blit(label, (350, i * 15))

    if (control_mode == CONTROL_WALK ):
        color = HIGHLIGHT
    else:
        color = WHITE
    label = myfont.render(ANIMATION[animation_frame], 1, color)
    screen.blit(label, (500, 50))

    if (walk_mode == WALK_RESET):
        message = "reset"
    elif (walk_mode == WALK_PAUSE):
        message = "pause"
    elif (walk_mode == WALK_PLAY):
        message = "walk"

    label = myfont.render(message, 1, color)
    screen.blit(label, (590, 30))


    pygame.display.flip()



#####################################
#           INITIALIZE              #
#####################################

mctransmitter.initialize()
pygame.init()
myfont = pygame.font.SysFont("monospace", 15, bold=True)
screen = pygame.display.set_mode((800, 200))
refresh()



#####################################
#              LOOP                 #
#####################################

while True:

    if (walk_mode == WALK_PLAY):
        frame += 1
        if ((frame % 10000) == 0):
            animation_frame = (animation_frame + 1)
            if (animation_frame >= len(ANIMATION)):
                animation_frame = ANIMATION_CONTINUE
            refresh()


    for event in pygame.event.get():

        # QUIT
        if ((event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == KEY_QUIT))):
            pygame.quit();


        # SWITCH COLUMN
        elif ((event.type == pygame.KEYDOWN) and (event.key == KEY_TAB)):
            control_mode = (control_mode + 1) % 3
            input_value = 0
            input_state = False


        # LEFT COLUMN
        elif (control_mode == CONTROL_MANUAL):
            if (event.type == pygame.KEYDOWN):
                if ((event.key == KEY_UP) and motorstate[current_motor] == 0):
                    current_motor = (current_motor - 1) % NUM_MOTORS
                elif ((event.key == KEY_DOWN) and motorstate[current_motor] == 0):
                    current_motor = (current_motor + 1) % NUM_MOTORS
                elif (event.key == KEY_LEFT):
                    if (motorstate[current_motor] == 0):
                        motorstate[current_motor] = 1
                        mctransmitter.tx_analog(current_motor, 1)
                elif (event.key == KEY_RIGHT):
                    if (motorstate[current_motor] == 0):
                        motorstate[current_motor] = 2
                        mctransmitter.tx_analog(current_motor, 2)
            elif (event.type == pygame.KEYUP):
                if ((event.key == KEY_LEFT) or (event.key == KEY_RIGHT)):
                    motorstate[current_motor] = 0
                    mctransmitter.tx_analog(current_motor, 0)


        # MIDDLE COLUMN
        elif (control_mode == CONTROL_TRANSMIT):
            if event.type == pygame.KEYDOWN:

                if (event.key == KEY_TRANSFER):
                    walk_mode = WALK_RESET
                    animation_frame = 0
                    transfer()

                elif (event.key == KEY_RETURN):
                    if (input_state):
                        if (input_value >= 0 and input_value <= VARIABLE_MAXS[highlighted_variable]):
                            variables[variable_names[highlighted_variable]] = input_value
                            highlighted_variable = (highlighted_variable + 1) % len(variables)
                        input_state = False
                    else:
                        input_value = 0
                        input_state = True

                # TYPING IN NEW VALUE
                elif (input_state and event.key >= 48 and event.key <= 57):
                    input_integer = event.key - 48
                    input_value = (input_value * 10) + input_integer

                elif (event.key == KEY_UP):
                    highlighted_variable = (highlighted_variable - 1) % len(variables)
                    input_value = 0
                    input_state = False
                elif (event.key == KEY_DOWN):
                    highlighted_variable = (highlighted_variable + 1) % len(variables)
                    input_value = 0
                    input_state = False


        # RIGHT COLUMN
        elif (control_mode == CONTROL_WALK):
            if ((event.type == pygame.KEYDOWN) and (event.key == KEY_SPACE)):
                if (walk_mode == WALK_PLAY):
                    walk_mode = WALK_PAUSE
                    mctransmitter.tx_analog(3, 0)
                elif (walk_mode == WALK_PAUSE):
                    walk_mode = WALK_PLAY
                    mctransmitter.tx_analog(3, 1)
                elif (walk_mode == WALK_RESET):
                    walk_mode = WALK_PLAY
                    mctransmitter.tx_analog(3, 1)


        refresh()
    mctransmitter.receive();
