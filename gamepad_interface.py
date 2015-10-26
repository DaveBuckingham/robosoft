# GAMEPAD INTERFACE
# Ethan Laverack
# Description: Uses PyGame library to pull data off of gamepad and send axis
#              and button states to ui_hub through standard out

# get the pygame library
import pygame

# initialize pygame
pygame.init()

#initalizes joystick module
pygame.joystick.init()

#
joysticks = pygame.joystick.get_count()
print str(joysticks) + " joystick(s) detected!"
