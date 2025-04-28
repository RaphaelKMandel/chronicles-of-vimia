from constants import *


class CommandState(State):
    KEYMAP = {
        "q": quit
    }

    def __init__(self, game):
        super().__init__(game)
        self.command = ""

    def handle_input(self, event):
        if event.key == pygame.K_RETURN:
            func = self.KEYMAP.get(self.command)
            if func: func()
            NormalMode(self.game)

        if event.type == pygame.KEYDOWN:
            self.command += event.unicode

    def draw(self):
        text_surface = FONT.render(f":{self.command}", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        self.game.screen.blit(text_surface, text_rect)


NormalMode.KEYMAP[":"] = CommandState
