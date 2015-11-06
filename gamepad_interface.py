'''
GAMEPAD INTERFACE
Ethan Laverack

Description: Uses PyGame joystick library to pull data off of gamepad and send axis
             and button states to ui_hub through standard out

FOR REFERENCE: https://www.pygame.org/docs/ref/joystick.html

INPUT: nothing, but needs gamepad plugged in to function
OUTPUT: prints button/axis states to standard out upon change

OUTPUT FORMAT:

gamepad_id# axis/button_id# value

    -prints new line with every event
    -Joysticks


OUTPUT BUTTON/AXIS ID NUMBERS:
    button_0 = A
    button_1 = B
    button_2 = X
    button_3 = Y
    button_4 = LeftBumper (LB)
    button_5 = RightBumper (RB)
    button_6 = Back
    button_7 = Start
    button_8 = Left Stick Click
    button_9 = Right Stick Click

    axis_0 = Left Stick X (1 = right)
    axis_1 = Left Stick Y (1 = down)
    axis_2 = Triggers (Left: 1, Right: -1, Niether: 0)
    axis_3 = Right Stick Y (1 = down)
    axis_4 = Right Stick X (1 = right)

    dpad_0 = D-Pad
        NOTE: Outputs as (1,1)

PyGame-xBox 360 Button/Axis Assignments:
    Buttons (1 for Pressed, 0 for not):
        0 = A
        1 = B
        2 = X
        3 = Y
        4 = LeftBumper (LB)
        5 = RightBumper (RB)
        6 = Back
        7 = Start
        8 = Left Stick Click
        9 = Right Stick Click
    Axis (range of values from -1 to 1):
        0 = Left Stick X (1 = right)
        1 = Left Stick Y (1 = down)
        2 = Triggers (Left: 1, Right: -1, Niether: 0)
        3 = Right Stick Y (1 = down)
        4 = Right Stick X (1 = right)
    D-Pad/Hat (Neither: (x,y) = (0,0)):
        0 = (right, up) = (1,1)
'''

# get the pygame library
import pygame

#initialize pygame & joystick module
pygame.init()

#initialize joysticks
pygame.joystick.init()


#function to detect gamepad disconnects - has issues
#from http://stackoverflow.com/questions/15802831/pygame-detect-joystick-disconnect-and-wait-for-it-to-be-reconnected
'''
discon = False
def check_pad():
    global discon
    pygame.joystick.quit()
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    if not joystick_count:
        if not discon:
           print "GAMEPAD DISCONNECTED"
           discon = True
    else:
        discon = False
'''

#checks for module initialize error
'''
if pygame.joystick.get_init():
    print 'Joystick Module Initialized'
else:
    print 'Module Initialize Error'
'''

#detect if joysticks are avaliable, let us know and initialize them
gamepad_count = pygame.joystick.get_count()
if gamepad_count:
#    print str(gamepad_count) + ' Gamepad(s) Detected'
    for i in range(gamepad_count):
        #creates a gamepad object instance using pygame Joystick class
        gamepad = pygame.joystick.Joystick(i)
        gamepad.init()
#        name = gamepad.get_name()
#        print 'Gamepad ' + str(i) + ' name: ' + name
else:
    print gamepad_count
    print 'No Gamepad Detected'

#boolean to exit the loop
exit = False

#axis 0 value area threshold
#0_THRESHOLD = 0.01
#axis_states[, prev_state = 0]

while gamepad_count and exit == False:
#    check_pad()
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print '{} button_{} {}'.format(event.joy, event.button, 1)
        if event.type == pygame.JOYBUTTONUP:
            print '{} button_{} {}'.format(event.joy, event.button, 0)
        if event.type == pygame.JOYAXISMOTION:
#          if (abs(event.value) < 0_THRESHOLD):
#            if (axis_states[
            print '{} axis_{} {}'.format(event.joy, event.axis, event.value)
        if event.type == pygame.JOYHATMOTION:
            print '{} dpad_{} {}'.format(event.joy, event.hat, event.value)
#included to stop the program during testing
#        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
#            exit = True

#quits pygame module & prevents "hanging"
pygame.quit()
