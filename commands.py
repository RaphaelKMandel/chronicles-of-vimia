from classes import *


class CommandMode(State):
    KEYMAP = {
        "q": EDITOR.quit,
        "w": EDITOR.write,
    }

    def __init__(self):
        super().__init__()
        self.command = ""

    def run_command(self):
        if self.command in self.KEYMAP:
            self.KEYMAP[self.command]()

        if self.command.startswith("e"):
            self.edit()

        if self.command.startswith("n"):
            self.restart()
            if isinstance(EDITOR.state, LostMode):
                EDITOR.state.restart = True
                EDITOR.state = EDITOR.states[-1]

    def handle_input(self, event):
        if event.key == pygame.K_RETURN:
            self.run_command()
            self.deactivate()

        if event.key == pygame.K_BACKSPACE:
            self.command = self.command[:-1]
            return

        if event.type == pygame.KEYDOWN:
            self.command += event.unicode

    def edit(self):
        buffer = self.command.split()[-1]
        if buffer in EDITOR.buffers:
            EDITOR.buffer = EDITOR.buffers[buffer]

    def restart(self):
        EDITOR.restart()

    def draw(self):
        text_surface = FONT.render(f":{self.command}", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        SCREEN.blit(text_surface, text_rect)


NormalMode.KEYMAP[":"] = CommandMode
LostMode.KEYMAP[":"] = CommandMode
