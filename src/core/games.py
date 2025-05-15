import sys

from .constants import *
from .modes import *


class Game:
    def __init__(self):
        self.running = True
        self.spawner = None
        self.multiplier = 1
        self.restart()

    def restart(self):
        self.lost = False
        self.puzzles = []
        self.command = ""
        self.last = ""
        self.credit = 25
        self.debit = 0

    def draw_command_line(self, text):
        # Line
        pygame.draw.rect(SCREEN, CURSOR_COLOR, (0, HEIGHT - CHAR_HEIGHT - BOTTOM, WIDTH, BOTTOM))

        # Status
        draw_text(text, 0, HEIGHT-CHAR_HEIGHT, TEXT_COLOR)

        # Last Command
        last = self.command if self.command else self.last
        draw_text(last, WIDTH // 2, HEIGHT - CHAR_HEIGHT, TEXT_COLOR)

        # Cursor Position Vector
        row, col = NVIM.funcs.getpos(".")[1:3]
        draw_text(f"{row}:{col}", WIDTH - 100, HEIGHT-CHAR_HEIGHT, TEXT_COLOR)

    def draw_top(self):
        draw_text(f"Score: {self.credit}", WIDTH - CHAR_WIDTH * 11, 0, WHITE)
        draw_text(f"Keys Remaining: {self.credit - self.debit}", WIDTH - CHAR_WIDTH * 20, CHAR_HEIGHT, WHITE)

    def draw(self):
        SCREEN.fill(BACKGROUND_COLOR)
        self.draw_top()
        self.draw_command_line(self.mode.NAME)
        for puzzle in self.puzzles:
            puzzle.draw()

        pygame.display.flip()

    def test(self):
        for puzzle in self.puzzles:
            puzzle.test()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                self.command += event.unicode
                print(self.mode.NAME, event.unicode)
                if self.mode.is_pending(self.command):
                    print("defering", self.command)
                    continue

                self.flush()

    @property
    def mode(self):
        if self.lost:
            return LostMode(self)

        mode = NVIM.eval("mode()")
        return {
            "n": NormalMode,
            "i": InsertMode,
            "v": VisualMode,
        }.get(mode, NormalMode)(self)

    @property
    def puzzle(self):
        return self.puzzles[0]

    def run(self):
        while self.running:
            self.handle_events()
            self.test()
            self.draw()
            if not self.lost:
                self.spawn()
                self.check_score()
            CLOCK.tick(FPS)

        self.quit()

    def spawn(self):
        self.spawner.spawn()

    def check_score(self):
        if self.credit <= self.debit:
            self.lost = True
            self.puzzles = []

    def flush(self):
        if self.command == ":q\r":
            self.quit()
            return

        if self.command == ":n\r":
            self.restart()
            return

        NVIM.input(self.command)
        self.last = self.command
        if not self.lost:
            self.debit += len(self.command)
        self.command = ""

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()
