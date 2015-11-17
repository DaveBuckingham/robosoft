"""
Gamepad Module
Daniel J. Gonzalez
dgonz@mit.edu

Based off code from: http://robots.dacloughb.com/project-1/logitech-game-pad/
"""

import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized Joystick : %s' % j.get_name()

"""
Returns a vector of the following form:
[LThumbstickX, LThumbstickY, Unknown Coupled Axis???,
RThumbstickX, RThumbstickY,
Button 1/X, Button 2/A, Button 3/B, Button 4/Y,
Left Bumper, Right Bumper, Left Trigger, Right Triller,
Select, Start, Left Thumb Press, Right Thumb Press]

Note:
No D-Pad.
Triggers are switches, not variable.
Your controller may be different
"""

def get():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    it = 0 #iterator
    pygame.event.pump()

    #Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it+=1
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it+=1
    return out

def test():
    while True:
        print get()
