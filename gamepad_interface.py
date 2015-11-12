'''
GAMEPAD INTERFACE
Ethan Laverack and David Buckingham

Description: Uses PyGame joystick library to pull data off of gamepad and send axis
             and button states to ui_hub through standard out

FOR REFERENCE: https://www.pygame.org/docs/ref/joystick.html

CONSULT global_data.py FOR DEFINITIONS -db

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
            #print '{} button_{} {}'.format(event.joy, event.button, 1)
            print '{} b {} {}'.format(event.joy, event.button, 1)  # -db
        if event.type == pygame.JOYBUTTONUP:
            #print '{} button_{} {}'.format(event.joy, event.button, 0)
            print '{} b {} {}'.format(event.joy, event.button, 0)  # -db
        if event.type == pygame.JOYAXISMOTION:
#          if (abs(event.value) < 0_THRESHOLD):
#            if (axis_states[
            #print '{} axis_{} {}'.format(event.joy, event.axis, event.value)
            print '{} a {} {}'.format(event.joy, event.axis, event.value)  # -db
        if event.type == pygame.JOYHATMOTION:
            #print '{} dpad_{} {}'.format(event.joy, event.hat, event.value)
            print '{} d {} {}'.format(event.joy, event.hat, event.value)  # -db
#included to stop the program during testing
#        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
#            exit = True

#quits pygame module & prevents "hanging"
pygame.quit()
