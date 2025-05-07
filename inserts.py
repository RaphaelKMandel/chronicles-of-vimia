from constants import *
from actions import Action, CompoundAction
from horizontal_movements import Right, Carrot, Dollar
from instant_actions import Backspace, Delete, InsertChar


class EnterInsertMode:
    def __init__(self, parent):
        self.parent = parent
        self.execute()

    def execute(self):
        self.state = InsertMode(self.parent)

    def get_actions(self):
        return self.state.actions


class LeaveInsertMode:
    def __init__(self, parent):
        self.parent = parent
        self.execute()

    def execute(self):
        EDITOR.state = self.parent


class InsertMode(State):
    KEYMAP = {}
    NAME = "-- INSERT --"

    def __init__(self, parent):
        super().__init__(parent)
        self.actions = []

    def max_col(self):
        return len(EDITOR.buffer.line)

    def handle_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.parent.deactivate()
            return

        if event.key == pygame.K_BACKSPACE:
            action = Backspace()
            action.execute()
            self.actions.append(action)
            # line, col = EDITOR.buffer.line, EDITOR.buffer.col
            # if col > 0:
            #     EDITOR.buffer.col -= 1
            #     EDITOR.buffer.line = line[:col - 1] + line[col:]
            #     return

        if event.key == pygame.K_DELETE:
            action = Delete()
            action.execute()
            self.actions.append(action)
            # line, col = EDITOR.buffer.line, EDITOR.buffer.col
            # EDITOR.buffer.line = line[:col] + line[col + 1:]

        if event.unicode.isprintable():
            action = InsertChar(event.unicode)
            action.execute()
            self.actions.append(action)
            # line, col = EDITOR.buffer.line, EDITOR.buffer.col
            # EDITOR.buffer.line = line[:col] + event.unicode + line[col:]
            # EDITOR.buffer.col += 1

    def draw(self):
        super().draw()

        # Draw cursor as a block
        top, left = EDITOR.buffer.get_coord(EDITOR.buffer.row, EDITOR.buffer.col)
        cursor_rect = pygame.Rect(left, top, CHAR_WIDTH // 4, CHAR_HEIGHT)

        # Draw the cursor
        pygame.draw.rect(EDITOR.screen, CURSOR_COLOR, cursor_rect)


class InsertAction(CompoundAction):
    def __init__(self, parent):
        super().__init__(parent)
        self.register()
        self.enter = EnterInsertMode(self)
        self.actions.append(self.enter)

    def deactivate(self):
        self.actions += self.enter.get_actions()
        self.actions.append(LeaveInsertMode(self.parent))


class AppendAction(InsertAction):
    def __init__(self, parent):
        super().__init__(parent)
        self.actions.append(Right(self))


class InsertAtStart(InsertAction):
    def __init__(self, parent):
        super().__init__(parent)
        self.actions.append(Carrot(self))


class AppendAtEnd(InsertAction):
    def __init__(self, parent):
        super().__init__(parent)
        self.actions.append(Dollar(self))


NormalMode.KEYMAP["i"] = InsertAction
NormalMode.KEYMAP["a"] = AppendAction
NormalMode.KEYMAP["I"] = InsertAtStart
NormalMode.KEYMAP["A"] = AppendAtEnd
