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
    def __call__(self):
        if Action.LAST_ACTION is not None:
            Action.LAST_ACTION.full_execute()

    def execute(self):
        Action.LAST_ACTION.execute()


class Replace(Action):
    def __init__(self):
        self.char = None
        CharState(self)

    def finish(self, char):
        if char.isprintable():
            self.char = char
            self.execute()

    def execute(self):
        if self.char is not None:
            col = EDITOR.buffer.col
            line = EDITOR.buffer.line
            EDITOR.buffer.line = line[:col] + self.char + line[col+1:]



NormalMode.KEYMAP["x"] = Delete()
NormalMode.KEYMAP["X"] = Backspace()
NormalMode.KEYMAP["."] = Period()
NormalMode.KEYMAP["r"] = Replace
