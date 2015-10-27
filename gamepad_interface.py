'''
GAMEPAD INTERFACE
Ethan Laverack

Description: Uses PyGame library to pull data off of gamepad and send axis
             and button states to ui_hub through standard out

xBox 360 Button/Axis Assignments:
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
    Axis (range of values from -1 to 1, 1 = down/right):
        0 = Left Stick X (1 = right)
        1 = Left Stick Y (1 = down)
        2 = Triggers (Left: 1, Right: -1, Niether: 0)
        3 = Right Stick Y (1 = down)
        4 = Right Stick X (1 = right)
    D-Pad/Hat (Neither: 0,0):
        Up = 1
        Right = 1
        Down = -1
        Left = -1
'''

# get the pygame library
import pygame

#initialize pygame & joystick module
pygame.init()

#initialize joysticks
pygame.joystick.init()
#checks for module initialize error
if pygame.joystick.get_init():
    print 'Joystick Module Initialized'
else:
    print 'Module Initialize Error'

#detect if joysticks are avaliable, let us know and initialize them
gamepad_count = pygame.joystick.get_count()
if gamepad_count:
    print str(gamepad_count) + ' Gamepad(s) Detected'
    for i in range(gamepad_count):
        #creates a gamepad object instance using pygame Joystick class
        gamepad = pygame.joystick.Joystick(i)
        gamepad.init()
        name = gamepad.get_name()
        print 'Gamepad ' + str(i) + ' name: ' + name

while pygame.joystick.get_count() == gamepad_count:
    for event in pygame.event.get():
        print 'things happening'



#replace default button numbers with easy variables

'''
Back =

while back == False:
    for event in pygame.event.get()
        if event.type == pygame.JOYBUTTONDOWN:
            print 'Button Pressed'
        if event.type == pygame.JOYBUTTONUP:
            print 'Button Released'
'''
#quits pygame module & prevents "hanging"
pygame.quit()
