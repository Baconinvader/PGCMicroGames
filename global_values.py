"""
This is a file for constants and global state.
You probably dont' need to look at this
"""
import pygame

#the current microgame being run
current_game = None

#the display surface
screen = None

#what part of the game we are at
state = "main_menu"

#list of controls (buttons, etc)
controls = []

#list of timers
timers = []

MICROGAME_TIMEOUT_EVENT = pygame.event.custom_type()
MICROGAME_END_EVENT = pygame.event.custom_type()
TEXT_BOX_DELETE_EVENT = pygame.event.custom_type()
RUN_GAME_EVENT = pygame.event.custom_type()

#CONSTANTS
WIDTH = 500
HEIGHT = 500

