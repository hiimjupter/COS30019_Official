import pygame

pygame.font.init()
EXPANDED_DELAY = 100
SCREEN_DELAY = 1500
CELL_SIZE = 40
BUTTON_WIDTH, BUTTON_HEIGHT = (200, 50)
SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GRAY": (149, 149, 149),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "ORANGE": (255, 215, 0)
}

SMALL_FONT = pygame.font.Font("OpenSans-Regular.ttf", 15)
MEDIUM_FONT = pygame.font.Font("OpenSans-Regular.ttf", 28)
LARGE_FONT = pygame.font.Font("OpenSans-Regular.ttf", 40)
