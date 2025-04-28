import pygame
import random
import sys
from vim_states import NormalState, State
from constants import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 200
FPS = 60
FONT_SIZE = 16
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
CURSOR_COLOR = (255, 255, 255)
CURSOR_TEXT_COLOR = (0, 0, 0)  # Text color when under cursor

# Try to load DejaVu Sans Mono, fall back to system monospace
FONT = pygame.font.SysFont("monospace", FONT_SIZE)

# Sample sentences
SAMPLE_SENTENCES = [
    "The (quick) brown fox, [jumps] over the {lazy} dog.",
]

class VimText:
    def __init__(self, text: str):
        self.text = text
        self.cursor_pos = 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vim Motions Practice")
        self.clock = pygame.time.Clock()
        self.font = FONT
        self.text = VimText(random.choice(SAMPLE_SENTENCES))
        self.state: State = NormalState()
        self.running = True

    def handle_input(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        else:
            self.state = self.state.handle_input(event, self)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw text
        text_surface = self.font.render(self.text.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text_surface, text_rect)
        
        # Draw cursor as a block
        if self.text.cursor_pos < len(self.text.text):
            char_width = self.font.size(self.text.text[self.text.cursor_pos])[0]
            cursor_x = text_rect.left + self.font.size(self.text.text[:self.text.cursor_pos])[0]
            cursor_rect = pygame.Rect(cursor_x, text_rect.top, char_width, text_rect.height)
            
            # Draw the cursor
            pygame.draw.rect(self.screen, CURSOR_COLOR, cursor_rect)
            
            # Draw the character under the cursor in a different color
            char_surface = self.font.render(self.text.text[self.text.cursor_pos], True, CURSOR_TEXT_COLOR)
            self.screen.blit(char_surface, (cursor_x, text_rect.top))
        else:
            # Handle cursor at end of line
            cursor_x = text_rect.left + self.font.size(self.text.text)[0]
            cursor_rect = pygame.Rect(cursor_x, text_rect.top, 2, text_rect.height)
            pygame.draw.rect(self.screen, CURSOR_COLOR, cursor_rect)

        # Draw state-specific elements
        self.state.draw(self)

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_input(event)

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 