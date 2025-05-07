from constants import *
from actions import InstantAction


class Delete:
    def execute(self):
        buffer = EDITOR.buffer
        line = buffer.line
        new_line = line[:buffer.col]
        if buffer.col < len(line) - 1:
            new_line += line[buffer.col + 1:]

        buffer.line = new_line
        buffer.col = buffer.col  # Needed to reset column to current column


class Backspace:
    def execute(self):
        buffer = EDITOR.buffer
        line = buffer.line
        buffer.line = line[:buffer.col - 1] + line[buffer.col:]
        buffer.col -= 1


class InsertChar:
    def __init__(self, char):
        self.char = char

    def execute(self):
        line, col = EDITOR.buffer.line, EDITOR.buffer.col
        EDITOR.buffer.line = line[:col] + self.char + line[col:]
        EDITOR.buffer.col += 1


class DeleteAction(InstantAction):
    execute = Delete.execute


class BackspaceAction(InstantAction):
    execute = Backspace.execute


def Period(parent):
    if EDITOR.last_action:
        print(EDITOR.last_action.actions)
        EDITOR.last_action.full_execute()


NormalMode.KEYMAP["x"] = DeleteAction
NormalMode.KEYMAP["X"] = BackspaceAction
NormalMode.KEYMAP["."] = Period
