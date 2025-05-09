from classes import *
from actions import Action, InstantAction


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


class InsertChar(InstantAction):
    def __init__(self, char):
        self.char = char

    def execute(self):
        line, col = EDITOR.buffer.line, EDITOR.buffer.col
        EDITOR.buffer.line = line[:col] + self.char + line[col:]
        EDITOR.buffer.col += 1


class Period(InstantAction):
    def __call__(self, parent):
        if Action.LAST_ACTION is not None:
            Action.LAST_ACTION.full_execute()

    def execute(self):
        Action.LAST_ACTION.execute()


NormalMode.KEYMAP["x"] = Delete()
NormalMode.KEYMAP["X"] = Backspace()
NormalMode.KEYMAP["."] = Period()
