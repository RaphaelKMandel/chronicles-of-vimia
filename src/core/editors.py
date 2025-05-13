import sys

from src.core.constants import *
from src.core.states import NormalMode, LostMode


class Editor:
    BOTTOM = 5

    def __init__(self):
        self.running = True
        self.spawner = None  # Must Define Spawner before executing run()
        self.states = []
        self.state = NormalMode(self)
        self.restart()

    def restart(self):
        self.lost = False
        self.debit = 0
        self.credit = 100
        self.buffers = {}
        self.history = ""
        self.states = [self.states[0]]

    @property
    def state(self):
        return self.states[-1]

    @state.setter
    def state(self, state):
        self.states.append(state)

    def pop(self):
        if len(self.states) > 1:
            self.states.pop()

    @property
    def buffer(self):
        if self.buffers:
            return list(self.buffers.values())[0]

    def draw_command_line(self, text):
        text_surface = FONT.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        SCREEN.blit(text_surface, text_rect)

        if self.buffer:
            coords = FONT.render(f"{self.buffer.row}:{self.buffer.col}", True, TEXT_COLOR)
            text_rect = coords.get_rect()
            text_rect.bottomleft = (WIDTH - 100, HEIGHT)
            SCREEN.blit(coords, text_rect)

        coords = FONT.render(f"{self.history}", True, TEXT_COLOR)
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
        header = FONT.render(f"Score: {self.credit}/{self.debit}", True, WHITE)
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
                self.debit += 1
                if event.unicode.isprintable():
                    self.history += event.unicode
                self.state.handle_input(event)
                print(self.history, self.state, event, self.credit, self.debit)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            CLOCK.tick(FPS)
            if not self.lost:
                self.spawn()
                self.check_score()

        self.quit()

    def spawn(self):
        if len(self.buffers) < 1:
            self.spawner.spawn()

    def check_score(self):
        if self.credit <= self.debit:
            self.lost = True
            LostMode(self)
            self.buffers = {}

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def write(self):
        self.buffer.test()
