from constants import *


class Command(State):
    def __init__(self, parent):
        super().__init__(parent)
        self.command = ""

    def init(self):
        """Initialize State Keybinds."""
        self.KEYMAP = {
            "q": self.quit,
            "w": self.write
        }

    def handle_input(self, event):
        if event.key == pygame.K_RETURN:
            func = self.KEYMAP.get(self.command)
            if func: func()
            self.deactivate()
            return

        if event.key == pygame.K_BACKSPACE:
            self.command = self.command[:-1]
            return

        if event.type == pygame.KEYDOWN:
            self.command += event.unicode

    def quit(self):
        EDITOR.quit()

    def write(self):
        EDITOR.write()

    def draw(self):
        text_surface = FONT.render(f":{self.command}", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        EDITOR.screen.blit(text_surface, text_rect)


Normal.KEYMAP[":"] = Command
