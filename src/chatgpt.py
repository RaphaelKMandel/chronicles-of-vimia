import sys
import pygame
import threading
from queue import Queue
import pynvim

from src.core.constants import *

# Initialize NVIM
NVIM = pynvim.attach('child', argv=["nvim", "--embed", "--headless"])

# Input queue for feeding keys into Neovim
key_queue = Queue()

def nvim_input_loop():
    while True:
        key = key_queue.get()
        try:
            NVIM.input(key)
        except Exception as e:
            print("NVIM input error:", e)

# Start the input thread
threading.Thread(target=nvim_input_loop, daemon=True).start()


def send(event):
    special_keys = {
        pygame.K_RETURN: "\r",
        pygame.K_BACKSPACE: "\b",
        pygame.K_ESCAPE: "\x1b",
        pygame.K_TAB: "\t",
        pygame.K_LEFT: "\x1bOD",
        pygame.K_RIGHT: "\x1bOC",
        pygame.K_UP: "\x1bOA",
        pygame.K_DOWN: "\x1bOB",
    }

    key = special_keys.get(event.key, event.unicode)
    if key:
        key_queue.put(key)


class State:
    def __init__(self, game):
        self.game = game
        self.game.state = self

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            send(event)


class NormalMode(State):
    pass


class Line:
    def __init__(self, text):
        self.text = text

    def draw(self, x, y):
        text_surface = FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(topleft=(x, y))
        SCREEN.blit(text_surface, text_rect)


class Buffer:
    def __init__(self, lines, x=20, y=20):
        self.x, self.y = x, y
        NVIM.command("enew")
        self.buffer = NVIM.current.buffer
        self.no = self.buffer.number
        NVIM.command("setlocal undolevels=-1")
        self.buffer[:] = lines
        NVIM.command("setlocal nomodified")
        NVIM.command("setlocal undolevels=100")

    @property
    def lines(self):
        return self.buffer[:]

    def get_pos(self):
        return NVIM.funcs.getpos('.')

    @property
    def row(self):
        return self.get_pos()[1]

    @property
    def col(self):
        return self.get_pos()[2]

    def width(self):
        return max([len(line) for line in self.lines])

    def height(self):
        return 2 * CHAR_HEIGHT * len(self.lines)

    def get_rect(self):
        return self.x, self.y, self.width() * CHAR_WIDTH, self.height()

    def draw(self):
        # Draw background
        pygame.draw.rect(SCREEN, WORD_BACKGROUND_COLOR, self.get_rect())

        # Draw text
        for n, line in enumerate(self.lines):
            line = Line(line)
            line.draw(self.x, self.y + (2 * n + 1) * CHAR_HEIGHT)

        # Animate falling
        dy = 10
        self.y += min(200, dy) / 60


class Game:
    def __init__(self):
        self.running = True
        self.buffers = {}
        self.states = []
        self.state = NormalMode(self)

    @property
    def state(self):
        return self.states[-1]

    @state.setter
    def state(self, state):
        self.states.append(state)

    def pop(self):
        if len(self.states) > 1:
            self.states.pop()

    def draw(self):
        SCREEN.fill(BACKGROUND_COLOR)
        for buffer in self.buffers.values():
            buffer.draw()

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            self.state.handle_events(event)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            CLOCK.tick(FPS)

        self.quit()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()


# Main entry point
game = Game()
game.buffers["a"] = Buffer(["this is some text"])
game.run()
