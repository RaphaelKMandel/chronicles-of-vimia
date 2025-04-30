import sys
import pygame

from dep.main import LINE_HEIGHT

# Initialize pygame
pygame.init()

# Game dimensions
WIDTH, HEIGHT = 800, 200
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


class Buffer:
    def __init__(self, lines: list[str], row=0, col=0):
        self.lines = lines
        self.row, self.col = row, col

    @property
    def col(self):
        return min(self._col, len(self.lines[self.row]) - 1)

    @col.setter
    def col(self, value):
        self._col = value

    def draw(self):
        # Draw text
        for n, line in enumerate(self.lines):
            text_surface = FONT.render(line, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(topleft=(20, 20 + n * LINE_HEIGHT))
            EDITOR.screen.blit(text_surface, text_rect)

            if self.row == n:
                # Draw cursor as a block
                char_width = FONT.size(line[self.col])[0]
                cursor_x = text_rect.left + FONT.size(line[:self.col])[0]
                cursor_rect = pygame.Rect(cursor_x, text_rect.top, char_width, text_rect.height)

                # Draw the cursor
                pygame.draw.rect(EDITOR.screen, CURSOR_COLOR, cursor_rect)

                # Draw the character under the cursor in a different color
                char_surface = FONT.render(self.lines[self.row][self.col], True, CURSOR_TEXT_COLOR)
                EDITOR.screen.blit(char_surface, (cursor_x, text_rect.top))

    def test(self):
        print("Testing buffer...")


class Editor:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chronicles of Vimia")
        self.clock = pygame.time.Clock()
        self.buffer = None
        self.state = None
        self.running = True
        self.last_operation = None
        self.last_search = None
        self.count = 0
        self.credit = 100

    def get_buffer(self, text):
        return Buffer(text)

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
        self.normal = Normal()
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


class State:
    def __init__(self, parent=None):
        self.parent = parent
        self.init()
        self.activate()

    def init(self):
        pass

    def activate(self):
        EDITOR.state = self

    def deactivate(self):
        if self.parent is None:
            raise ValueError(f"Cannot deactivate {self}; no parent state exists")

        self.parent.activate()

    def handle_input(self, event):
        if event.unicode in self.KEYMAP:
            self.KEYMAP[event.unicode](self)
        else:
            print(f"Unknown keybind {event.unicode} in {EDITOR.state}.")
            self.deactivate()

    def draw(self):
        text_surface = FONT.render(self.__class__.__name__, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        EDITOR.screen.blit(text_surface, text_rect)


class Normal(State):
    KEYMAP = {}

    def deactivate(self):
        pass


class Insert(State):
    KEYMAP = {}


class Visual(State):
    KEYMAP = {}


class Movement:
    def __init__(self, parent):
        lines = EDITOR.buffer.lines
        row = EDITOR.buffer.row
        col = EDITOR.buffer.col
        self.execute(lines, row, col)

    def execute(self, lines, row, col):
        raise NotImplementedError(f"execute() method of Movement is not implemented.")

    @staticmethod
    def evaluate(lines, row, col):
        raise NotImplementedError(f"evaluate() method of Movement is not implemented.")


EDITOR = Editor()
