from classes import *
from inserts import InsertActionBase
from motions import StartWord, EndWord, PrevWord, Find
from actions import Action


class OperatorMode(NormalMode):
    KEYMAP = {}

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.motion = None

    def handle_input(self, event):
        command = self.get_command(event)
        if command is not None:
            command(self)

    def finish(self, motion):
        EDITOR.pop()
        self.parent.finish(motion)


class OperatorAction(Action):
    def __init__(self):
        super().__init__()
        self.register()
        self.motion = None
        OperatorMode(self)

    def finish(self, motion):
        self.motion = motion
        self.execute()


class DeleteOperator(OperatorAction):
    def execute(self):
        buffer = EDITOR.buffer
        row, col = buffer.row, buffer.col
        new_row, new_col = self.motion.evaluate(buffer)
        if row == new_row and new_col is not None:
            if col > new_col:
                col, new_col = new_col, col

            new_col += 1
            line = buffer.line
            buffer.line = line[:col] + line[new_col:]
            buffer.col = col


class ChangeOperator(DeleteOperator):
    def __init__(self):
        super().__init__()
        self.insert = None

    def finish(self, motion):
        self.motion = motion
        super().execute()
        self.insert = InsertActionBase()

    def execute(self):
        super().execute()
        self.insert.execute()


class FindAction:
    def __init__(self, parent, motion):
        self.parent = parent
        self.motion = motion

    def finish(self):
        self.parent.finish(self)

    def evaluate(self, buffer):
        col = self.motion.evaluate(buffer)
        return buffer.row, col


class FindForwardAction(FindAction):
    def __init__(self, parent):
        super().__init__(parent, Find(self, forward=True, offset=0))


class FindBackwardAction(FindAction):
    def __init__(self, parent):
        super().__init__(parent, Find(self, forward=False, offset=0))


class FindForwardToAction(FindAction):
    def __init__(self, parent):
        super().__init__(parent, Find(self, forward=True, offset=1))


class FindBackwardToAction(FindAction):
    def __init__(self, parent):
        super().__init__(parent, Find(self, forward=False, offset=1))


class StartWordAction:
    def __init__(self, parent):
        self.parent = parent
        self.motion = StartWord()
        self.parent.finish(self)

    def evaluate(self, buffer):
        col = self.motion.evaluate(buffer) - 1
        return buffer.row, col


class EndWordAction:
    def __init__(self, parent):
        self.parent = parent
        self.motion = EndWord()
        self.parent.finish(self)

    def evaluate(self, buffer):
        col = self.motion.evaluate(buffer)
        return buffer.row, col


class PrevWordAction:
    def __init__(self, parent):
        self.parent = parent
        self.motion = PrevWord()
        self.parent.finish(self)

    def evaluate(self, buffer):
        col = self.motion.evaluate(buffer)
        return buffer.row, col


NormalMode.KEYMAP["d"] = DeleteOperator
NormalMode.KEYMAP["c"] = ChangeOperator

OperatorMode.KEYMAP["f"] = FindForwardAction
OperatorMode.KEYMAP["F"] = FindBackwardAction
OperatorMode.KEYMAP["t"] = FindForwardToAction
OperatorMode.KEYMAP["T"] = FindBackwardToAction

OperatorMode.KEYMAP["w"] = StartWordAction
OperatorMode.KEYMAP["e"] = EndWordAction
OperatorMode.KEYMAP["b"] = PrevWordAction
