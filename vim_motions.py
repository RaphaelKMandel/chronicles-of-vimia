import pygame
import random
import sys
import re

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
        # Pre-calculate word boundaries for both types of motions
        self.word_boundaries = self._calculate_word_boundaries()
        self.big_word_boundaries = self._calculate_big_word_boundaries()

    def _calculate_word_boundaries(self):
        # Find all word boundaries (including punctuation)
        boundaries = []
        # Match words including punctuation that's part of the word (like apostrophes, hyphens)
        # but treat other punctuation as separate words
        for match in re.finditer(r'[a-zA-Z0-9\'\-]+|[^\s]', self.text):
            boundaries.append((match.start(), match.end()))
        return boundaries

    def _calculate_big_word_boundaries(self):
        # Find all big word boundaries (only whitespace)
        boundaries = []
        # Match any non-whitespace sequence
        for match in re.finditer(r'\S+', self.text):
            boundaries.append((match.start(), match.end()))
        return boundaries

    def _find_next_boundary(self, boundaries, current_pos, forward=True):
        if forward:
            for start, end in boundaries:
                if start > current_pos:
                    return start
            return len(self.text)
        else:
            for start, end in reversed(boundaries):
                if end <= current_pos:
                    return start
            return 0

    def _find_end_boundary(self, boundaries, current_pos):
        # First check if we're already at the end of a word
        for start, end in boundaries:
            if start <= current_pos < end:
                # If we're at the end of this word, move to the end of the next word
                if current_pos == end - 1:
                    for next_start, next_end in boundaries:
                        if next_start > current_pos:
                            return next_end - 1
                    return len(self.text)
                # Otherwise move to the end of the current word
                return end - 1
        # If we're not in a word, find the next word's end
        for start, end in boundaries:
            if start > current_pos:
                return end - 1
        return len(self.text)

    def move_cursor(self, motion: str, char: str = None):
        if motion == 'h' and self.cursor_pos > 0:
            self.cursor_pos -= 1
        elif motion == 'l' and self.cursor_pos < len(self.text):
            self.cursor_pos += 1
        elif motion == 'w':  # Move to start of next word (punctuation as boundary)
            self.cursor_pos = self._find_next_boundary(self.word_boundaries, self.cursor_pos)
        elif motion == 'W':  # Move to start of next WORD (only whitespace as boundary)
            self.cursor_pos = self._find_next_boundary(self.big_word_boundaries, self.cursor_pos)
        elif motion == 'e':  # Move to end of current word (punctuation as boundary)
            self.cursor_pos = self._find_end_boundary(self.word_boundaries, self.cursor_pos)
        elif motion == 'E':  # Move to end of current WORD (only whitespace as boundary)
            self.cursor_pos = self._find_end_boundary(self.big_word_boundaries, self.cursor_pos)
        elif motion == 'b':  # Move to start of current/previous word (punctuation as boundary)
            self.cursor_pos = self._find_next_boundary(self.word_boundaries, self.cursor_pos, False)
        elif motion == 'B':  # Move to start of current/previous WORD (only whitespace as boundary)
            self.cursor_pos = self._find_next_boundary(self.big_word_boundaries, self.cursor_pos, False)
        elif motion == '$':  # Move to end of line
            self.cursor_pos = len(self.text)
        elif motion == '^' or motion == '_':  # Move to first non-blank character
            # Find first non-whitespace character
            for i, char in enumerate(self.text):
                if not char.isspace():
                    self.cursor_pos = i
                    break
        elif motion == 'f' and char:  # Move to next occurrence of char
            pos = self.text.find(char, self.cursor_pos + 1)
            if pos != -1:
                self.cursor_pos = pos
        elif motion == 'F' and char:  # Move to previous occurrence of char
            pos = self.text.rfind(char, 0, self.cursor_pos)
            if pos != -1:
                self.cursor_pos = pos
        elif motion == 't' and char:  # Move to before next occurrence of char
            pos = self.text.find(char, self.cursor_pos + 1)
            if pos != -1:
                self.cursor_pos = pos - 1
        elif motion == 'T' and char:  # Move to after previous occurrence of char
            pos = self.text.rfind(char, 0, self.cursor_pos)
            if pos != -1:
                self.cursor_pos = pos + 1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vim Motions Practice")
        self.clock = pygame.time.Clock()
        self.font = FONT
        self.text = VimText(random.choice(SAMPLE_SENTENCES))
        self.find_mode = False
        self.till_mode = False
        self.backward_mode = False
        self.command_mode = False
        self.command_buffer = ""
        self.running = True

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.find_mode = False
                self.till_mode = False
                self.backward_mode = False
                self.command_mode = False
                self.command_buffer = ""
            elif self.command_mode:
                if event.unicode.isprintable():
                    self.command_buffer += event.unicode
                elif event.key == pygame.K_RETURN:
                    if self.command_buffer == "q":
                        self.running = False
                    self.command_mode = False
                    self.command_buffer = ""
            elif self.find_mode or self.till_mode:
                if event.unicode.isprintable():
                    motion = 'F' if self.backward_mode else 'f'
                    if self.till_mode:
                        motion = motion.lower()  # 'f' becomes 't', 'F' becomes 'T'
                    self.text.move_cursor(motion, event.unicode)
                self.find_mode = False
                self.till_mode = False
                self.backward_mode = False
            else:
                if event.unicode == ':':
                    self.command_mode = True
                    self.command_buffer = ""
                elif event.unicode == 'h':
                    self.text.move_cursor('h')
                elif event.unicode == 'l':
                    self.text.move_cursor('l')
                elif event.unicode == 'w':
                    self.text.move_cursor('w')
                elif event.unicode == 'W':
                    self.text.move_cursor('W')
                elif event.unicode == 'e':
                    self.text.move_cursor('e')
                elif event.unicode == 'E':
                    self.text.move_cursor('E')
                elif event.unicode == 'b':
                    self.text.move_cursor('b')
                elif event.unicode == 'B':
                    self.text.move_cursor('B')
                elif event.unicode == '$':
                    self.text.move_cursor('$')
                elif event.unicode == '^':
                    self.text.move_cursor('^')
                elif event.unicode == '_':
                    self.text.move_cursor('_')
                elif event.unicode == 'f':
                    self.find_mode = True
                    self.backward_mode = False
                elif event.unicode == 'F':
                    self.find_mode = True
                    self.backward_mode = True
                elif event.unicode == 't':
                    self.till_mode = True
                    self.backward_mode = False
                elif event.unicode == 'T':
                    self.till_mode = True
                    self.backward_mode = True

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

        # Draw mode indicator
        if self.find_mode or self.till_mode:
            mode_text = ""
            if self.backward_mode:
                mode_text += "F" if self.find_mode else "T"
            else:
                mode_text += "f" if self.find_mode else "t"
            mode_surface = self.font.render(mode_text, True, CURSOR_COLOR)
            self.screen.blit(mode_surface, (10, 10))
        elif self.command_mode:
            command_text = self.font.render(f":{self.command_buffer}", True, CURSOR_COLOR)
            self.screen.blit(command_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 