import pygame
import random
import sys
from typing import List, Tuple

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT_SIZE = 24
LINE_HEIGHT = 30
FALL_SPEED = 0.5
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
CURSOR_COLOR = (0, 255, 0)
INSERT_MODE_COLOR = (255, 0, 0)
DELETE_COLOR = (255, 0, 0)
COMMAND_COLOR = (0, 255, 255)
MAX_LINES = 5

# Sample text lines with commands and text to delete
SAMPLE_TEXT = [
    {"text": "Hello, world!", "to_delete": "world"},
    {"text": "Vim is awesome!", "to_delete": "is"},
    {"text": "Practice makes perfect", "to_delete": "makes"},
    {"text": "The quick brown fox", "to_delete": "quick"},
    {"text": "Jump over the lazy dog", "to_delete": "lazy"},
    {"text": "Python is fun", "to_delete": "is"},
    {"text": "Game development", "to_delete": "ment"},
    {"text": "Learn Vim motions", "to_delete": "Learn"},
    {"text": "Type faster", "to_delete": "faster"},
    {"text": "Edit efficiently", "to_delete": "Edit"}
]

class TextLine:
    def __init__(self, line_number: int, text: str, to_delete: str, x: int, y: int):
        self.line_number = line_number
        self.command = f":{line_number}"
        self.text = text
        self.to_delete = to_delete
        self.x = x
        self.y = y
        self.cursor_pos = 0
        self.insert_mode = False
        self.delete_start = text.find(to_delete)
        self.delete_end = self.delete_start + len(to_delete)
        self.words = text.split()

    def move_cursor(self, direction: str, char: str = None):
        if direction == 'h' and self.cursor_pos > 0:
            self.cursor_pos -= 1
        elif direction == 'l' and self.cursor_pos < len(self.text):
            self.cursor_pos += 1
        elif direction == 'w':  # Move to next word
            current_word_end = 0
            for word in self.words:
                word_start = self.text.find(word, current_word_end)
                word_end = word_start + len(word)
                if word_start > self.cursor_pos:
                    self.cursor_pos = word_start
                    break
                current_word_end = word_end
            if self.cursor_pos == current_word_end:  # If at last word, move to end
                self.cursor_pos = len(self.text)
        elif direction == 'f' and char:  # Find character
            pos = self.text.find(char, self.cursor_pos + 1)
            if pos != -1:
                self.cursor_pos = pos

    def insert_char(self, char: str):
        if self.insert_mode:
            self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
            self.cursor_pos += 1
            # Update delete positions if text changed
            self.delete_start = self.text.find(self.to_delete)
            self.delete_end = self.delete_start + len(self.to_delete)
            self.words = self.text.split()

    def delete_char(self):
        if self.cursor_pos > 0:
            self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1
            # Update delete positions if text changed
            self.delete_start = self.text.find(self.to_delete)
            self.delete_end = self.delete_start + len(self.to_delete)
            self.words = self.text.split()

    def delete_word(self):
        if self.cursor_pos < len(self.text):
            # Find the end of the current word
            word_end = self.cursor_pos
            while word_end < len(self.text) and self.text[word_end] != ' ':
                word_end += 1
            # Delete the word
            self.text = self.text[:self.cursor_pos] + self.text[word_end:]
            # Update delete positions if text changed
            self.delete_start = self.text.find(self.to_delete)
            self.delete_end = self.delete_start + len(self.to_delete)
            self.words = self.text.split()

    def delete_line(self):
        self.text = ""
        self.cursor_pos = 0
        self.delete_start = -1
        self.delete_end = -1
        self.words = []

    def is_completed(self) -> bool:
        return self.delete_start == -1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vim Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.lines: List[TextLine] = []
        self.current_line = 0
        self.insert_mode = False
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 3000
        self.command_buffer = ""
        self.command_mode = False
        self.find_mode = False
        self.used_line_numbers = set()
        self.running = True

    def get_next_line_number(self):
        # Find the smallest unused line number
        line_number = 1
        while line_number in self.used_line_numbers:
            line_number += 1
        self.used_line_numbers.add(line_number)
        return line_number

    def spawn_line(self):
        if len(self.lines) < MAX_LINES:
            text_data = random.choice(SAMPLE_TEXT)
            x = random.randint(100, WIDTH - 100)
            line_number = self.get_next_line_number()
            self.lines.append(TextLine(
                line_number,
                text_data["text"],
                text_data["to_delete"],
                x, 0
            ))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.insert_mode = False
                self.command_mode = False
                self.find_mode = False
                self.command_buffer = ""
                if self.lines:
                    self.lines[self.current_line].insert_mode = False
            elif self.insert_mode:
                if event.unicode.isprintable():
                    self.lines[self.current_line].insert_char(event.unicode)
            elif self.command_mode:
                if event.unicode.isdigit():
                    self.command_buffer += event.unicode
                elif event.key == pygame.K_RETURN:
                    if self.command_buffer == "q":
                        self.running = False
                    else:
                        try:
                            target_line = int(self.command_buffer)
                            # Find line with matching number
                            for i, line in enumerate(self.lines):
                                if line.line_number == target_line:
                                    self.current_line = i
                                    self.score += 10
                                    break
                        except ValueError:
                            pass
                    self.command_mode = False
                    self.command_buffer = ""
            elif self.find_mode:
                if event.unicode.isprintable():
                    self.lines[self.current_line].move_cursor('f', event.unicode)
                self.find_mode = False
            else:
                if event.unicode == 'i':
                    self.insert_mode = True
                    if self.lines:
                        self.lines[self.current_line].insert_mode = True
                elif event.unicode == ':':
                    self.command_mode = True
                    self.command_buffer = ""
                elif event.unicode == 'f':
                    self.find_mode = True
                elif event.unicode == 'h':
                    if self.lines:
                        self.lines[self.current_line].move_cursor('h')
                elif event.unicode == 'l':
                    if self.lines:
                        self.lines[self.current_line].move_cursor('l')
                elif event.unicode == 'w':
                    if self.lines:
                        self.lines[self.current_line].move_cursor('w')
                elif event.unicode == 'x':
                    if self.lines:
                        self.lines[self.current_line].delete_char()
                elif event.unicode == 'd':
                    if pygame.key.get_pressed()[pygame.K_w]:
                        if self.lines:
                            self.lines[self.current_line].delete_word()
                    elif pygame.key.get_pressed()[pygame.K_d]:
                        if self.lines:
                            self.lines[self.current_line].delete_line()

    def update(self):
        # Move lines down
        for line in self.lines:
            line.y += FALL_SPEED

        # Check for completed lines and remove them
        for line in self.lines[:]:
            if line.is_completed():
                self.score += 100
                self.used_line_numbers.remove(line.line_number)
                self.lines.remove(line)

        # Remove lines that have fallen off screen
        for line in self.lines[:]:
            if line.y >= HEIGHT:
                self.used_line_numbers.remove(line.line_number)
                self.lines.remove(line)

        # Spawn new lines
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > self.spawn_interval:
            self.spawn_line()
            self.spawn_timer = current_time

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw lines
        for i, line in enumerate(self.lines):
            # Draw command
            command_surface = self.font.render(line.command, True, COMMAND_COLOR)
            self.screen.blit(command_surface, (line.x - 50, line.y))

            # Draw text with highlighted deletion
            if line.delete_start >= 0:
                # Draw text before deletion
                before_text = line.text[:line.delete_start]
                before_surface = self.font.render(before_text, True, TEXT_COLOR)
                self.screen.blit(before_surface, (line.x, line.y))

                # Draw text to delete
                delete_text = line.text[line.delete_start:line.delete_end]
                delete_surface = self.font.render(delete_text, True, DELETE_COLOR)
                delete_x = line.x + self.font.size(before_text)[0]
                self.screen.blit(delete_surface, (delete_x, line.y))

                # Draw text after deletion
                after_text = line.text[line.delete_end:]
                after_surface = self.font.render(after_text, True, TEXT_COLOR)
                after_x = delete_x + self.font.size(delete_text)[0]
                self.screen.blit(after_surface, (after_x, line.y))
            else:
                # Draw entire text if no deletion needed
                color = INSERT_MODE_COLOR if line.insert_mode else TEXT_COLOR
                text_surface = self.font.render(line.text, True, color)
                self.screen.blit(text_surface, (line.x, line.y))
            
            # Draw cursor
            if i == self.current_line:
                cursor_x = line.x + self.font.size(line.text[:line.cursor_pos])[0]
                cursor_width = 1 if line.insert_mode else 3
                pygame.draw.line(self.screen, CURSOR_COLOR,
                               (cursor_x, line.y),
                               (cursor_x, line.y + LINE_HEIGHT),
                               cursor_width)

        # Draw command buffer
        if self.command_mode:
            command_text = self.font.render(f":{self.command_buffer}", True, COMMAND_COLOR)
            self.screen.blit(command_text, (10, HEIGHT - 30))
        elif self.find_mode:
            command_text = self.font.render("f", True, COMMAND_COLOR)
            self.screen.blit(command_text, (10, HEIGHT - 30))

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 