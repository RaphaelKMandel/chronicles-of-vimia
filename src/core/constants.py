import pygame
import pynvim

# Initialize pynvim
NVIM = pynvim.attach('child', argv=["nvim", "--embed", "--headless", "--clean"])
NVIM.command("set noswapfile")

# Initialize pygame
pygame.init()
pygame.display.set_caption("Chronicles of Vimia")

# Repeat keys
pygame.key.set_repeat(600, 50)

# Game dimensions
WIDTH, HEIGHT = 1600, 900
FPS = 60
FONT_SIZE = 32
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BOTTOM = 5

# Game Objects
CLOCK = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
CURSOR_COLOR = (255, 255, 255)
CURSOR_TEXT_COLOR = (0, 0, 0)  # Text color when under cursor
WORD_BACKGROUND_COLOR = (32, 0, 106)

# Font
FONT = pygame.font.SysFont("monospace", FONT_SIZE)
if "agave" in pygame.font.get_fonts():
    FONT = pygame.font.SysFont("agave", FONT_SIZE)

CHAR_WIDTH, CHAR_HEIGHT = FONT.size(" ")


def get_pos():
    return NVIM.funcs.getpos(".")

def draw_text(text, x, y, color):
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.bottomleft = (x, y)
    SCREEN.blit(text_surface, text_rect)
