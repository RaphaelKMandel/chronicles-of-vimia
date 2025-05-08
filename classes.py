import sys

from pygame import K_ESCAPE

from constants import *
from spawners import RandomSpawner


class Child:
    def __init__(self, parent):
        self.parent = parent


class Editor:
    BOTTOM = 5

    def __init__(self):
        pygame.display.set_caption("Chronicles of Vimia")
        self.clock = pygame.time.Clock()
        self.state = None
        self.running = True
        self.last_action = None
        self.last_search = None
        self.spawner = RandomSpawner(self)
        self.lost = False
        self.count = 0
        self.credit = 20
        self.buffers = {}

    @property
    def buffer(self):
        if self.buffers:
            return list(self.buffers.values())[0]

    def restart(self):
        self.lost = False
        self.count = 0
        self.credit = 20
        self.buffers = {}

    def draw_command_line(self, text):
        text_surface = FONT.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        SCREEN.blit(text_surface, text_rect)

        if self.buffer:
            coords = FONT.render(f"{self.buffer.row}:{self.buffer.col}", True, TEXT_COLOR)
            text_rect = coords.get_rect()
            text_rect.bottomleft = (WIDTH // 2, HEIGHT)
            SCREEN.blit(coords, text_rect)

    def draw(self):
        SCREEN.fill(BACKGROUND_COLOR)
        for buffer in list(self.buffers.values()):
            buffer.test()
        for buffer in self.buffers.values():
            buffer.draw()
        if self.state: self.state.draw()
        self.draw_score()
        self.draw_bottom()
        pygame.display.flip()

    def draw_score(self):
        header = FONT.render(f"Score: {self.credit}/{self.count}", True, WHITE)
        header_rect = header.get_rect(topleft=(WIDTH - CHAR_WIDTH * 16, 0))
        SCREEN.blit(header, header_rect)

    def draw_bottom(self):
        pygame.draw.rect(SCREEN, CURSOR_COLOR, (0, HEIGHT - CHAR_HEIGHT - Editor.BOTTOM, WIDTH, Editor.BOTTOM))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return

            if event.type == pygame.KEYDOWN and not event.unicode == "":
                self.count += 1
                print(self.state, event, self.credit, self.count)
                self.state.handle_input(event)

    def run(self):
        self.normal = NormalMode()
        self.state = self.normal
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
            if not self.lost:
                self.spawn()
                self.check_score()

        self.quit()

    def spawn(self):
        if len(self.buffers) < 1:
            self.spawner.spawn()

    def check_score(self):
        if self.credit <= self.count:
            self.lost = True
            LostMode(self.normal)
            self.buffers = {}

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

    def get_command(self, event):
        if event.key == K_ESCAPE:
            self.deactivate()
            return

        if event.unicode in self.KEYMAP:
            print(self, event.unicode, self.KEYMAP[event.unicode])
            return self.KEYMAP[event.unicode]

        print(f"Unknown keybind {event.unicode} in {EDITOR.state}.")

    def handle_input(self, event):
        command = self.get_command(event)
        if command is not None:
            command(self)

    def draw(self):
        EDITOR.draw_command_line(self.NAME)


class NormalMode(State):
    KEYMAP = {}
    NAME = "NORMAL"

    def max_col(self):
        return len(EDITOR.buffer.line) - 1

    def draw(self):
        super().draw()

        # Draw cursor as a block
        if EDITOR.buffer:
            top, left = EDITOR.buffer.get_coord(EDITOR.buffer.row, EDITOR.buffer.col)
            cursor_rect = pygame.Rect(left, top, CHAR_WIDTH, CHAR_HEIGHT)

            # Draw the cursor
            pygame.draw.rect(SCREEN, CURSOR_COLOR, cursor_rect)

            # Draw the character under the cursor in a different color
            char_surface = FONT.render(EDITOR.buffer.line[EDITOR.buffer.col], True, CURSOR_TEXT_COLOR)
            SCREEN.blit(char_surface, (left, top))


class LostMode(State):
    KEYMAP = {}
    NAME = "GAME OVER"

    def __init__(self, parent):
        super().__init__(parent)
        self.restart = False

    def max_col(self):
        return 0


class BufferMemento:
    """Used to save state for undo/redo."""

    def __init__(self, buffer):
        self.lines = [line.text for line in buffer.lines]
        self.row = buffer.row
        self.col = buffer.col

    def restore(self, buffer):
        for line, text in zip(buffer.lines, self.lines):
            line.text = text

        buffer.row, buffer.col = self.row, self.col


class Movement(Child):
    def execute(self):
        pass

    def evaluate(self, buffer):
        pass


class InstantMovement(Movement):
    def __init__(self, parent):
        super().__init__(parent)
        self.execute()


EDITOR = Editor()
