from constants import *
from commands import CommandState
from movements import *


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chronicles of Vimia")
        self.clock = pygame.time.Clock()
        self.buffer = self.get_buffer("This is (the) sample text(s).")
        self.state = NormalMode(self)

    def get_buffer(self, text):
        return Buffer(self, text)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.buffer.draw()
        self.state.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.state.handle_input(event)

    def run(self):
        while RUNNING:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        quit()


class Buffer:
    def __init__(self, game, text: str, row=0, col=0):
        self.game = game
        self.text = text
        self.row, self.col = row, col

    def draw(self):
        # Draw text
        text_surface = FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.game.screen.blit(text_surface, text_rect)

        # Draw cursor as a block
        char_width = FONT.size(self.text[self.col])[0]
        cursor_x = text_rect.left + FONT.size(self.text[:self.col])[0]
        cursor_rect = pygame.Rect(cursor_x, text_rect.top, char_width, text_rect.height)

        # Draw the cursor
        pygame.draw.rect(self.game.screen, CURSOR_COLOR, cursor_rect)

        # Draw the character under the cursor in a different color
        char_surface = FONT.render(self.text[self.col], True, CURSOR_TEXT_COLOR)
        self.game.screen.blit(char_surface, (cursor_x, text_rect.top))


if __name__ == "__main__":
    game = Game()
    game.run()
