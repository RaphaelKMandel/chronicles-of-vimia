from constants import *


class InstantAction(Action):
    def __init__(self, parent):
        super().__init__(parent)
        self.activate()


class Delete(InstantAction):
    def execute(self):
        buffer = EDITOR.buffer
        line = buffer.line
        new_line = line[:buffer.col]
        if buffer.col < len(line) - 1:
            new_line += line[buffer.col + 1:]

        buffer.line = new_line
        buffer.col = buffer.col  # Needed to reset column to current column


class Backspace(InstantAction):
    def execute(self):
        buffer = EDITOR.buffer
        line = buffer.line
        buffer.line = line[:buffer.col - 1] + line[buffer.col:]

        buffer.col -= 1


def Period(parent):
    if EDITOR.last_action:
        EDITOR.last_action.execute()


NormalMode.KEYMAP["x"] = Delete
NormalMode.KEYMAP["X"] = Backspace
NormalMode.KEYMAP["."] = Period
