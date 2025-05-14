import sys

from src.core.constants import *
from src.core.buffers import Buffer
from src.core.modes import *


class Game:
    def __init__(self):
        self.running = True
        self.buffers = {}
        self.command = ""
        self.credit = 100
        self.debit = 0

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

            if event.type == pygame.KEYDOWN:
                self.command += event.unicode
                self.mode = self.get_mode()
                print(self.mode, event.unicode)
                if self.mode.eval():
                    print("defering", self.command)
                    continue

                self.flush()

    def get_mode(self):
        mode = NVIM.eval("mode()")
        return {
            "n": NormalMode,
            "i": InsertMode,
            "v": VisualMode,
        }.get(mode, NormalMode)(self, self.command)

    def run(self):
        while self.running:
            self.handle_events()
            for buffer in self.buffers.values():
                buffer.test()
            self.draw()
            CLOCK.tick(FPS)

        self.quit()

    def flush(self):
        NVIM.input(self.command)
        self.command = ""

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()


game = Game()
game.buffers["a"] = Buffer(game, ["this is some text"], ["This isnt some text"])
game.run()
