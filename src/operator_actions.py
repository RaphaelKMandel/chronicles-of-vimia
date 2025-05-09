from classes import *
from finds import FindForward, FindBackward, FindForwardTo, FindBackwardTo
from actions import CompoundAction


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


class OperatorAction(CompoundAction):
    def __init__(self):
        super().__init__()
        self.register()
        self.motion = None
        self.state = OperatorMode(self)

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
        super().__init__(parent, FindForward(self))


class FindBackwardAction(FindAction):
    def __init__(self, parent):
        super().__init__(parent, FindBackward(self))


class FindForwardToAction(FindAction):
    def __init__(self, parent):
        super().__init__(parent, FindForwardTo(self))


class FindBackwardToAction(FindAction):
    def __init__(self, parent):
        super().__init__(parent, FindBackwardTo(self))


NormalMode.KEYMAP["d"] = DeleteOperator
OperatorMode.KEYMAP["f"] = FindForwardAction
OperatorMode.KEYMAP["F"] = FindBackwardAction
OperatorMode.KEYMAP["t"] = FindForwardToAction
OperatorMode.KEYMAP["T"] = FindBackwardToAction
