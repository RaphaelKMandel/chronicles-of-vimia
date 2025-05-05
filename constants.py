import sys
import pygame
import difflib

# Initialize pygame
pygame.init()

# Repeat keys
pygame.key.set_repeat(500, 50)

# Game dimensions
WIDTH, HEIGHT = 1600, 900
FPS = 60
FONT_SIZE = 32

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
CURSOR_COLOR = (255, 255, 255)
CURSOR_TEXT_COLOR = (0, 0, 0)  # Text color when under cursor

# Font
FONT = pygame.font.SysFont("monospace", FONT_SIZE)
if "agave" in pygame.font.get_fonts():
    FONT = pygame.font.SysFont("agave", FONT_SIZE)

CHAR_WIDTH, CHAR_HEIGHT = FONT.size(" ")


class Child:
    def __init__(self, parent):
        self.parent = parent


class Line:
    COLORS = {
        "insert": GREEN,
        "equal": WHITE,
        "delete": RED
    }

    def __len__(self):
        return len(self.text)

    def __getitem__(self, item):
        return self.text[item]

    def __init__(self, text, target):
        self.augmented = ""
        self.map = []
        self.words = []
        self.target = target
        self.text = text

    def is_solved(self):
        return self.text == self.target

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.update()

    def update(self):
        self.words = self.get_diff()
        self.augmented = "".join([string for _, string in self.words])
        self.get_map()

    def get_map(self):
        self.map = [None] * (len(self.text) + 2)
        n1 = n2 = 0
        for word in self.words:
            if word[0] in {"equal", "delete"}:
                for _ in word[1]:
                    self.map[n1] = n2
                    n1 += 1
                    n2 += 1

            else:
                n2 += len(word[1])

        self.map[n1] = n2
        self.map[n1+1] = n2+1


    def get_diff(self):
        words = []
        x = difflib.SequenceMatcher(a=self.text, b=self.target).get_opcodes()
        for op, s1, f1, s2, f2 in x:
            if op == "replace":
                words.append(
                    ("delete", self.text[s1:f1])
                )
                words.append(
                    ("insert", self.target[s2:f2])
                )
            else:
                words.append(
                    (op, self.target[s2:f2])
                )

        return words

    def get_coord(self, row, col):
        return CHAR_WIDTH * col, CHAR_HEIGHT * row

    def get_x_coord(self, col):
        return CHAR_WIDTH * self.map[col]

    def draw(self, x, y):
        col = 0
        for op, string in self.words:
            text_surface = FONT.render(string, True, Line.COLORS[op])
            text_rect = text_surface.get_rect(topleft=(x + CHAR_WIDTH * col, y))
            EDITOR.screen.blit(text_surface, text_rect)
            col += len(string)


class Buffer:
    def __init__(self, lines: list[Line], row=0, col=0, x=20, y=20):
        self.lines = lines
        self.row, self.col = row, col
        self.x, self.y = x, y
        self.undo_list = []
        self.redo_list = []

    def get_coord(self, row, col):
        return (
            self.y + row * CHAR_HEIGHT,
            self.x + self.lines[row].map[col] * CHAR_WIDTH
        )

    @property
    def col(self):
        max_col = EDITOR.state.max_col()
        return min(self._col, max_col)

    @col.setter
    def col(self, value):
        self._col = value

    @property
    def line(self):
        return self.lines[self.row].text

    @line.setter
    def line(self, value):
        self.lines[self.row].text = value

    def get_topleft(self, row):
        return self.x, self.y + row * CHAR_HEIGHT

    def draw(self):
        # Draw text
        for n, line in enumerate(self.lines):
            line.draw(self.x, self.y + CHAR_HEIGHT * n)

        self.y += 0.1

    def test(self):
        print("Testing buffer...")
        if all([line.is_solved() for line in self.lines]):
            EDITOR.credit += 100
            print("Solved!")

        else:
            print("Not solved!")

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

    def get_buffer(self, lines, targets=None):
        if targets is None:
            return Buffer([Line(line) for line in lines])

        return Buffer([Line(line, target) for line, target in zip(lines, targets)])

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
            if event.type == pygame.QUIT:
                self.quit()
                return

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

    def max_col(self):
        return len(EDITOR.buffer.line)

    def draw(self):
        super().draw()

        # Draw cursor as a block
        top, left = EDITOR.buffer.get_coord(EDITOR.buffer.row, EDITOR.buffer.col)
        cursor_rect = pygame.Rect(left, top, CHAR_WIDTH, CHAR_HEIGHT)

        # Draw the cursor
        pygame.draw.rect(EDITOR.screen, CURSOR_COLOR, cursor_rect)

        # Draw the character under the cursor in a different color
        char_surface = FONT.render(EDITOR.buffer.line[EDITOR.buffer.col], True, CURSOR_TEXT_COLOR)
        EDITOR.screen.blit(char_surface, (left, top))


class InsertMode(State):
    KEYMAP = {}
    NAME = "-- INSERT --"

    def max_col(self):
        return len(EDITOR.buffer.line) + 1

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

    def draw(self):
        super().draw()

        # Draw cursor as a block
        top, left = EDITOR.buffer.get_coord(EDITOR.buffer.row, EDITOR.buffer.col)
        cursor_rect = pygame.Rect(left, top, CHAR_WIDTH // 4, CHAR_HEIGHT)

        # Draw the cursor
        pygame.draw.rect(EDITOR.screen, CURSOR_COLOR, cursor_rect)


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
