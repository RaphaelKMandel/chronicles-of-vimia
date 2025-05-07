from constants import *
from horizontal_movements import Carrot, Dollar

class InsertMode(State):
    KEYMAP = {}
    NAME = "-- INSERT --"

    def max_col(self):
        return len(EDITOR.buffer.line)

    def handle_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.deactivate()
            return

        if event.key == pygame.K_BACKSPACE:
            line, col = EDITOR.buffer.line, EDITOR.buffer.col
            if col > 0:
                EDITOR.buffer.col -= 1
                EDITOR.buffer.line = line[:col - 1] + line[col:]
                return

        if event.key == pygame.K_DELETE:
            line, col = EDITOR.buffer.line, EDITOR.buffer.col
            EDITOR.buffer.line = line[:col] + line[col + 1:]
            return

        if event.unicode.isprintable():
            line, col = EDITOR.buffer.line, EDITOR.buffer.col
            EDITOR.buffer.line = line[:col] + event.unicode + line[col:]
            EDITOR.buffer.col += 1

    def draw(self):
        super().draw()

        # Draw cursor as a block
        top, left = EDITOR.buffer.get_coord(EDITOR.buffer.row, EDITOR.buffer.col)
        cursor_rect = pygame.Rect(left, top, CHAR_WIDTH // 4, CHAR_HEIGHT)

        # Draw the cursor
        pygame.draw.rect(EDITOR.screen, CURSOR_COLOR, cursor_rect)

class Insert(Action):
    def __init__(self, parent):
        super().__init__(parent)
        InsertMode(parent)


class Append(Action):
    def __init__(self, parent):
        super().__init__(parent)
        EDITOR.buffer.col += 1
        InsertMode(parent)


class InsertAtStart(Action):
    def __init__(self, parent):
        super().__init__(parent)
        EDITOR.buffer.col = Carrot(parent).evaluate(EDITOR.buffer)
        Insert(parent)


class AppendAtEnd(Action):
    def __init__(self, parent):
        super().__init__(parent)
        EDITOR.buffer.col = Dollar(parent).evaluate(EDITOR.buffer)
        Append(parent)


NormalMode.KEYMAP["i"] = Insert
NormalMode.KEYMAP["a"] = Append
NormalMode.KEYMAP["I"] = InsertAtStart
NormalMode.KEYMAP["A"] = AppendAtEnd
