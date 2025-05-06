from constants import *


class Command(State):
    KEYMAP = {
        "q": EDITOR.quit,
        "w": EDITOR.write,
    }
    def __init__(self, parent):
        super().__init__(parent)
        self.command = ""

    def get_command(self):
        if self.command in self.KEYMAP:
            self.KEYMAP[self.command]()

        if self.command.startswith("e"):
            self.edit()

    def handle_input(self, event):
        if event.key == pygame.K_RETURN:
            self.get_command()
            self.deactivate()
            return

        if event.key == pygame.K_BACKSPACE:
            self.command = self.command[:-1]
            return

        if event.type == pygame.KEYDOWN:
            self.command += event.unicode

    def edit(self):
        buffer = self.command.split()[-1]
        if buffer in EDITOR.buffers:
            EDITOR.buffer = EDITOR.buffers[buffer]

    def draw(self):
        text_surface = FONT.render(f":{self.command}", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        EDITOR.screen.blit(text_surface, text_rect)


NormalMode.KEYMAP[":"] = Command
