from src.core.constants import *


class State:
    NAME = "NORMAL"

    def __init__(self, editor):
        self.editor = editor
        self.activate()

    def activate(self):
        self.editor.state = self

    def deactivate(self):
        self.editor.pop()

    def max_col(self):
        return len(self.editor.buffer.line) - 1

    def get_command(self, event):
        if event.key == pygame.K_ESCAPE:
            self.deactivate()
            return

        if event.unicode in self.KEYMAP:
            print(self, event.unicode, self.KEYMAP[event.unicode])
            return self.KEYMAP[event.unicode]

        print(f"Unknown keybind {event.unicode} in {self.editor.state}.")

    def handle_input(self, event):
        command = self.get_command(event)
        if command is not None:
            command(self.editor)

    def draw(self):
        self.editor.draw_command_line(self.NAME)


class NormalMode(State):
    KEYMAP = {}

    def handle_input(self, event):
        if event.unicode.isprintable():
            self.editor.history = event.unicode

        super().handle_input(event)

    def draw(self):
        super().draw()
        # Draw cursor as a block
        if self.editor.buffer:
            top, left = self.editor.buffer.get_coord(self.editor.buffer.row, self.editor.buffer.col)
            cursor_rect = pygame.Rect(left, top, CHAR_WIDTH, CHAR_HEIGHT)

            # Draw the cursor
            pygame.draw.rect(SCREEN, CURSOR_COLOR, cursor_rect)

            # Draw the character under the cursor in a different color
            char_surface = FONT.render(self.editor.buffer.line[self.editor.buffer.col], True, CURSOR_TEXT_COLOR)
            SCREEN.blit(char_surface, (left, top))


class CharMode(State):
    def __init__(self, editor, parent):
        super().__init__(editor)
        self.parent = parent

    def handle_input(self, event):
        self.finish(event.unicode)

    def finish(self, char):
        self.editor.pop()
        self.parent.finish(char)


class LostMode(State):
    KEYMAP = {}
    NAME = "GAME OVER"

    def __init__(self, editor):
        super().__init__(editor)
        self.editor.history = ""
        self.restart = False

    def max_col(self):
        return 0


class CommandMode(State):
    KEYMAP = {}

    def quit(self):
        self.editor.quit()

    def write(self):
        self.editor.write()

    def __init__(self, editor):
        super().__init__(editor)
        self.command = ""
        self.KEYMAP["q"] = self.quit
        self.KEYMAP["w"] = self.write

    def run_command(self):
        if self.command in self.KEYMAP:
            self.KEYMAP[self.command]()

        if self.command.startswith("e"):
            self.edit()

        if self.command.startswith("n"):
            self.restart()
            if isinstance(self.editor.state, LostMode):
                self.editor.state.restart = True
                self.editor.state = self.editor.states[-1]

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
        if buffer in self.editor.buffers:
            self.editor.buffer = self.editor.buffers[buffer]

    def restart(self):
        self.editor.restart()

    def draw(self):
        text_surface = FONT.render(f":{self.command}", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (0, HEIGHT)
        SCREEN.blit(text_surface, text_rect)


NormalMode.KEYMAP[":"] = CommandMode
LostMode.KEYMAP[":"] = CommandMode
