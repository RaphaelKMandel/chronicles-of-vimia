from classes import *
from actions import CompoundAction
from finds import FindForward


class OperatorMode(NormalMode):
    KEYMAP = {}

    def handle_input(self, event):
        self.parent.motion = self.get_command(event)(self)


class OperatorAction(CompoundAction):
    def __init__(self, parent):
        super().__init__(parent)
        self.movement = None
        self.state = OperatorMode(self)

    def activate(self):
        if self.movement is not None:
            self.full_execute()
            self.deactivate()

    def deactivate(self):
        self.parent.activate()


class DeleteOperator(OperatorAction):
    def execute(self):
        buffer = EDITOR.buffer
        row, col = buffer.row, buffer.col
        new_row, new_col = self.movement.evaluate(buffer)
        if row == new_row and new_col is not None:
            line = buffer.line
            buffer.line = line[:col] + line[new_col:]


class FindForwardAction(FindForward):
    def deactivate(self):
        self.parent.parent.activate()

    def activate(self):
        self.deactivate()

    def evaluate(self, buffer):
        col = self.forward_search(buffer)
        print("forward search", col)
        return buffer.row, col


NormalMode.KEYMAP["d"] = DeleteOperator
OperatorMode.KEYMAP["f"] = FindForwardAction
