from classes import *
from actions import Action, CompoundAction
from horizontal_movements import MoveRight, MoveCarrot, MoveDollar
from instant_actions import Backspace, Delete, InsertChar


class EnterInsertMode:
    def __init__(self, parent):
        self.parent = parent

    def execute(self):
        self.state = InsertMode(self)

    def finish(self):
        self.parent.finish(self.state.actions)


class LeaveInsertMode:
    def execute(self):
        EDITOR.pop()


class InsertMode(State):
    KEYMAP = {}
    NAME = "-- INSERT --"

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.actions = []

    def max_col(self):
        return len(EDITOR.buffer.line)

    def handle_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.parent.finish()
            return

        if event.key == pygame.K_BACKSPACE:
            action = Backspace()
            action.execute()
            self.actions.append(action)

        if event.key == pygame.K_DELETE:
            action = Delete()
            action.execute()
            self.actions.append(action)

        if event.unicode.isprintable():
            action = InsertChar(event.unicode)
            action.execute()
            self.actions.append(action)

    def draw(self):
        super().draw()

        # Draw cursor as a block
        top, left = EDITOR.buffer.get_coord(EDITOR.buffer.row, EDITOR.buffer.col)
        cursor_rect = pygame.Rect(left, top, CHAR_WIDTH // 4, CHAR_HEIGHT)

        # Draw the cursor
        pygame.draw.rect(SCREEN, CURSOR_COLOR, cursor_rect)


class InsertAction(CompoundAction):
    def __init__(self):
        super().__init__()
        self.register()
        action = EnterInsertMode(self)
        self.actions.append(action)
        action.execute()

    def finish(self, actions):
        self.actions += actions
        action = LeaveInsertMode()
        self.actions.append(action)
        action.execute()


class SubsAction(CompoundAction):
    def __init__(self):
        super().__init__()
        self.register()
        action = Delete()
        self.actions.append(action)
        action.execute()
        action = EnterInsertMode(self)
        self.actions.append(action)
        action.execute()

    def finish(self, actions):
        self.actions += actions
        action = LeaveInsertMode()
        self.actions.append(action)
        action.execute()


class AppendAction(InsertAction):
    def __init__(self):
        super().__init__()
        action = MoveRight()
        self.actions.append(action)
        action.execute()


class InsertAtStart(InsertAction):
    def __init__(self):
        super().__init__()
        action = MoveCarrot()
        self.actions.append(action)
        action.execute()


class AppendAtEnd(InsertAction):
    def __init__(self):
        super().__init__()
        action = MoveDollar()
        self.actions.append(action)
        action.execute()


NormalMode.KEYMAP["i"] = InsertAction
NormalMode.KEYMAP["a"] = AppendAction
NormalMode.KEYMAP["s"] = SubsAction
NormalMode.KEYMAP["I"] = InsertAtStart
NormalMode.KEYMAP["A"] = AppendAtEnd
