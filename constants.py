import sys
import pygame

# Initialize pygame
pygame.init()

# Game dimensions
WIDTH, HEIGHT = 800, 200
FPS = 60
FONT_SIZE = 16

# Colors
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
CURSOR_COLOR = (255, 255, 255)
CURSOR_TEXT_COLOR = (0, 0, 0)  # Text color when under cursor

# Font
FONT = pygame.font.SysFont("monospace", FONT_SIZE)


RUNNING = True

def quit():
    global RUNNING
    RUNNING = False
    pygame.quit()
    sys.exit()


class State:
    KEYMAP = {}
    def __init__(self, game):
        self.game = game
        self.game.state = self
        print(self.__class__.__name__)

    def handle_input(self, event):
        self.KEYMAP.get(event.unicode, NormalMode)(self.game)

    def draw(self):
        pass


class NormalMode(State):
    KEYMAP = {}


class InsertMode(State):
    KEYMAP = {}


class VisualMode(State):
    KEYMAP = {}