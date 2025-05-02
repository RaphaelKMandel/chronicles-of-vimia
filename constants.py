import sys
import pygame
from abc import ABC, abstractmethod

# Initialize pygame
pygame.init()

# Repeat keys
pygame.key.set_repeat(500, 50)

# Game dimensions
WIDTH, HEIGHT = 1600, 900
FPS = 60
FONT_SIZE = 32

# Colors
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
CURSOR_COLOR = (255, 255, 255)
CURSOR_TEXT_COLOR = (0, 0, 0)  # Text color when under cursor

# Font
FONT = pygame.font.SysFont("agave", FONT_SIZE)
LINE_HEIGHT = FONT.get_linesize()


class Child:
    def __init__(self, parent):
        self.parent = parent


class Buffer:
    def __init__(self, lines: list[str], row=0, col=0, x=0, y=0):
        self.lines = lines
        self.row, self.col = row, col
        self.x, self.y = x, y
        self.undo_list = []
        self.redo_list = []

    @property
    def col(self):
        max_col = len(self.line) - 1 if isinstance(EDITOR.state, NormalMode) else len(self.line)
        return min(self._col, max_col)

    @col.setter
    def col(self, value):
        self._col = value

    @property
    def line(self):
        return self.lines[self.row]

    @line.setter
    def line(self, value):
        self.lines[self.row] = value

    def get_topleft(self, row):
        return self.x + 20, self.y + 20 + row * LINE_HEIGHT

    def draw(self):
        # Draw text
        for n, line in enumerate(self.lines):
            text_surface = FONT.render(line, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(topleft=self.get_topleft(n))
            EDITOR.screen.blit(text_surface, text_rect)

            if self.row == n:
                # Draw cursor as a block
                char_width = FONT.size(line[0])[0]
                if isinstance(EDITOR.state, InsertMode):
                    char_width //= 4
                cursor_x = text_rect.left + FONT.size(line[:self.col])[0]
                cursor_rect = pygame.Rect(cursor_x, text_rect.top, char_width, text_rect.height)

                # Draw the cursor
                pygame.draw.rect(EDITOR.screen, CURSOR_COLOR, cursor_rect)

                # Draw the character under the cursor in a different color
                if not isinstance(EDITOR.state, InsertMode):
                    char_surface = FONT.render(self.line[self.col], True, CURSOR_TEXT_COLOR)
                    EDITOR.screen.blit(char_surface, (cursor_x, text_rect.top))

    def test(self):
        print("Testing buffer...")

    def copy(self):
        return Buffer(self.lines.copy(), row=self.row, col=self.col)


class Editor:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chronicles of Vimia")
        self.clock = pygame.time.Clock()
        self.buffer = None
        self.state = None
        self.running = True
        self.last_action = None
        self.last_search = None
        self.count = 0
        self.credit = 100

    def get_buffer(self, text):
        return Buffer(text)

    def draw_command_line(self, text):
        text_surface = FONT.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        EDITOR.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        if self.buffer: self.buffer.draw()
        if self.state: self.state.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and not event.unicode == "":
                self.count += 1
                print(event, self.count, self.credit - self.count)
                self.state.handle_input(event)

    def run(self):
        self.normal = NormalMode()
        self.state = self.normal
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        self.quit()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def write(self):
        self.buffer.test()


class State(Child):
    NAME = "None"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.activate()

    def activate(self):
        EDITOR.state = self

    def deactivate(self):
        if self.parent is not None:
            self.parent.activate()

    def handle_input(self, event):
        if event.unicode in self.KEYMAP:
            self.KEYMAP[event.unicode](self)
        else:
            print(f"Unknown keybind {event.unicode} in {EDITOR.state}.")
            self.deactivate()

    def draw(self):
        EDITOR.draw_command_line(self.NAME)


class NormalMode(State):
    KEYMAP = {}
    NAME = "NORMAL"


class InsertMode(State):
    KEYMAP = {}
    NAME = "-- INSERT --"

    def handle_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.deactivate()
            return

        if event.key == pygame.K_BACKSPACE:
            line, col = EDITOR.buffer.line, EDITOR.buffer.col
            if col > 0:
                EDITOR.buffer.col -= 1
                EDITOR.buffer.line = line[:col - 1] + line[col:]
                return

        if event.key == pygame.K_DELETE:
            line, col = EDITOR.buffer.line, EDITOR.buffer.col
            EDITOR.buffer.line = line[:col] + line[col + 1:]
            return

        if event.unicode.isprintable():
            line, col = EDITOR.buffer.line, EDITOR.buffer.col
            EDITOR.buffer.line = line[:col] + event.unicode + line[col:]
            EDITOR.buffer.col += 1


class Movement(Child):
    def execute(self):
        pass

    def evaluate(self, buffer):
        pass


class InstantMovement(Movement):
    def __init__(self, parent):
        super().__init__(parent)
        self.execute()


class Action(Child):
    def activate(self):
        EDITOR.buffer.undo_list.append(EDITOR.buffer.copy())
        EDITOR.buffer.redo_list = []
        self.execute()
        EDITOR.state = self.parent
        EDITOR.last_action = self

    def execute(self):
        pass


EDITOR = Editor()
