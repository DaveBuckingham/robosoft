#!/usr/bin/python

# BY DAVE, FOR TESTING GAITS

import time
import os
import sys
import pygame
import collections
import serial
import struct


EXPAND = 0
CONTRACT = 1

NUM_MOTORS = 4

TRANSMIT_DELAY = 0.8  # SECONDS

# TOGGLED WITH THE <TAB> KEY
CONTROL_MANUAL = 0
CONTROL_TRANSMIT = 1
CONTROL_WALK = 2

# ROBOT MOVING?
WALK_RESET = 0
WALK_PAUSE = 1
WALK_PLAY = 2

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





# FOR UI
current_motor = 0
selected_row = 0
selected_col = 0

# FOR MANUAL MOTOR CONTROL
motorstate = [0] * NUM_MOTORS   # 0->stopped   1->expanding    2->contracting

control_mode = CONTROL_MANUAL

walk_mode = WALK_RESET

input_state = False   # ENTERING A VARIABLE
input_value = 0       # VARIABLE VALUE BEING ENTERED

frame = 0            # COUNTER FOR ANIMATION
animation_frame = 0  # POINTS TO ASCII ART

vars = collections.OrderedDict()

vars['expanded_delay']  = ([6000] * NUM_MOTORS) 
vars['contract_time']   = ([6000] * NUM_MOTORS) 
vars['contracted_delay']= ([6000] * NUM_MOTORS) 
vars['expand_time']     = ([6000] * NUM_MOTORS) 
vars['contract_speed']  = ([100]  * NUM_MOTORS) 
vars['expand_speed']    = ([100]  * NUM_MOTORS) 
vars['offset']          = ([0] * NUM_MOTORS) 

VARIABLE_MAXS = [60000, 60000, 60000, 60000, 255, 255, 60000]


# INITIALIZE SERIAL connection
connection = None

if (os.name == 'posix'):
    port_name = '/dev/ttyACM0'
else:
    port_name = 'COM4'  

connection = serial.Serial(
    port=port_name,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0   # don't block when reading
)


def load():
    print "Loading saved gait."
    try:
        f = open('gait.dat', 'r')
        for var in vars.items():
            for i in range(0, NUM_MOTORS):
                var[1][i] = int(f.readline())
    except:
        print "Failed to load saved gait. Using defaults."

def save():
    f = open('gait.dat', 'w')
    for var in vars.items():
        for i in range(0, NUM_MOTORS):
            f.write(str(var[1][i]))
            f.write("\n")



def transfer():
    packed = struct.pack('!c', 't')
    connection.write(packed)
    for i in range(0, NUM_MOTORS):
        packed = struct.pack('!HHHHBBH', vars['expanded_delay'][i], \
                                         vars['contract_time'][i], \
                                         vars['contracted_delay'][i], \
                                         vars['expand_time'][i], \
                                         vars['contract_speed'][i], \
                                         vars['expand_speed'][i], \
                                         vars['offset'][i])
        connection.write(packed)




def refresh():
    screen.fill((0,0,0))
    draw_text()
    draw_graphs()
    pygame.display.flip()


def draw_text():
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
        screen.blit(label, (0, (i * 15) + 30))



    for col in range(0, NUM_MOTORS):
        string = 'm' + str(col)
        label = myfont.render('m' + str(col), 1, WHITE)
        screen.blit(label, (390 + (col * 60), 5))

    row = 0;
    for var in vars.items():
        label = myfont.render(var[0], 1, WHITE)
        screen.blit(label, (200, (row * 15) + 30))

        for col in range(0, NUM_MOTORS):


            if (row == selected_row and col == selected_col and control_mode == CONTROL_TRANSMIT):
                if (input_state):
                    label = myfont.render(str(input_value), 1, HIGHLIGHT)
                else:
                    label = myfont.render(str(var[1][col]), 1, HIGHLIGHT)
            else:
                label = myfont.render(str(var[1][col]), 1, WHITE)
            screen.blit(label, (380 + (col * 60), (row * 15) + 30))

        row += 1


    if (control_mode == CONTROL_WALK ):
        color = HIGHLIGHT
    else:
        color = WHITE
    label = myfont.render(ANIMATION[animation_frame], 1, color)
    screen.blit(label, (700, 60))

    if (walk_mode == WALK_RESET):
        message = "reset"
    elif (walk_mode == WALK_PAUSE):
        message = "pause"
    elif (walk_mode == WALK_PLAY):
        message = "walk"

    label = myfont.render(message, 1, color)
    screen.blit(label, (790, 30))



# HARD CODED FOR 4 MOTORS
def draw_graphs():

    motor_y = []
    for i in range (0, NUM_MOTORS):
        motor_y.append(200 + (100 * i))
    
    GRAPH_HEIGHT = 60

    GRAPH_WIDTH = 800

    max_cycle = 0
    for i in range (0, NUM_MOTORS):
        cycle = vars['offset'][i]   + \
                vars['expanded_delay'][i]   + \
                vars['contract_time'][i]    + \
                vars['contracted_delay'][i] + \
                vars['expand_time'][i]

        max_cycle = max(max_cycle, cycle)
    

    scale = GRAPH_WIDTH / float(max_cycle)

    MARGIN = 80


    for i in range(0, NUM_MOTORS):

        label = myfont.render('m' + str(i), 1, WHITE)
        screen.blit(label, (MARGIN - 40, motor_y[i]))

        motor_lines = []

        x_pos = ((vars['offset'][i] % max_cycle) * scale) + MARGIN
        motor_lines.append((x_pos, motor_y[i]))

        x_pos += ((vars['expanded_delay'][i] % max_cycle) * scale)
        motor_lines.append((x_pos, motor_y[i]))

        x_pos += ((vars['contract_time'][i] % max_cycle) * scale)
        motor_lines.append((x_pos, motor_y[i] + GRAPH_HEIGHT))

        x_pos += ((vars['contracted_delay'][i] % max_cycle) * scale)
        motor_lines.append((x_pos, motor_y[i] + GRAPH_HEIGHT))

        x_pos += ((vars['expand_time'][i] % max_cycle) * scale)
        motor_lines.append((x_pos, motor_y[i]))


        pygame.draw.lines(screen, WHITE, False, motor_lines)

    label = myfont.render(str(max_cycle) + 'ms', 1, WHITE)
    screen.blit(label, (GRAPH_WIDTH + 40, 600))





#####################################
#           INITIALIZE              #
#####################################

pygame.init()
myfont = pygame.font.SysFont("monospace", 17, bold=True)
screen = pygame.display.set_mode((1000, 800))
load()
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
            save()
            pygame.quit()
            sys.exit()


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
                        connection.write(struct.pack('!cBB', 'a', current_motor, 1))
                elif (event.key == KEY_RIGHT):
                    if (motorstate[current_motor] == 0):
                        motorstate[current_motor] = 2
                        connection.write(struct.pack('!cBB', 'a', current_motor, 2))
            elif (event.type == pygame.KEYUP):
                if ((event.key == KEY_LEFT) or (event.key == KEY_RIGHT)):
                    motorstate[current_motor] = 0
                    connection.write(struct.pack('!cBB', 'a', current_motor, 0))


        # MIDDLE COLUMN
        elif (control_mode == CONTROL_TRANSMIT):
            if event.type == pygame.KEYDOWN:

                if (event.key == KEY_TRANSFER):
                    walk_mode = WALK_RESET
                    animation_frame = 0
                    transfer()

                elif (event.key == KEY_RETURN):
                    if (input_state):
                        if (input_value >= 0 and input_value <= VARIABLE_MAXS[selected_col]):
                            # THERE IS DEFINATELY A BETTER WAY TO DO THIS
                            vars[vars.items()[selected_row][0]][selected_col] = input_value
                        input_state = False
                    else:
                        input_value = 0
                        input_state = True

                # TYPING IN NEW VALUE
                elif (input_state and event.key >= 48 and event.key <= 57):
                    input_integer = event.key - 48
                    input_value = (input_value * 10) + input_integer

                elif (event.key == KEY_UP):
                    selected_row = (selected_row - 1) % len(vars)
                    input_value = 0
                    input_state = False
                elif (event.key == KEY_DOWN):
                    selected_row = (selected_row + 1) % len(vars)
                    input_value = 0
                    input_state = False
                elif (event.key == KEY_LEFT):
                    selected_col = (selected_col - 1) % NUM_MOTORS
                    input_value = 0
                    input_state = False
                elif (event.key == KEY_RIGHT):
                    selected_col = (selected_col + 1) % NUM_MOTORS
                    input_value = 0
                    input_state = False


        # RIGHT COLUMN
        elif (control_mode == CONTROL_WALK):
            if ((event.type == pygame.KEYDOWN) and (event.key == KEY_SPACE)):
                if (walk_mode == WALK_PLAY):
                    walk_mode = WALK_PAUSE
                    connection.write(struct.pack('!cB', 'p', 0))
                elif (walk_mode == WALK_PAUSE):
                    walk_mode = WALK_PLAY
                    connection.write(struct.pack('!cB', 'p', 1))
                elif (walk_mode == WALK_RESET):
                    walk_mode = WALK_PLAY
                    connection.write(struct.pack('!cB', 'p', 1))


        refresh()

    line = connection.readline()
    if (len(line) > 0):
        sys.stdout.write(line);
