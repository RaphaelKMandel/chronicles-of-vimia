from constants import *
from horizontal_movements import Carrot, Dollar


class Insert(Action):
    def __init__(self, parent):
        self.parent = parent
        InsertMode(parent)


class Append:
    def __init__(self, parent):
        self.parent = parent
        EDITOR.buffer.col += 1
        InsertMode(parent)


class InsertAtStart(Action):
    def __init__(self, parent):
        self.parent = parent
        EDITOR.buffer.col = Carrot(parent).evaluate(EDITOR.buffer.lines, EDITOR.buffer.row, EDITOR.buffer.col)
        Insert(parent)


class AppendAtEnd(Action):
    def __init__(self, parent):
        self.parent = parent
        EDITOR.buffer.col = Dollar(parent).evaluate(EDITOR.buffer.lines, EDITOR.buffer.row, EDITOR.buffer.col)
        Append(parent)


NormalMode.KEYMAP["i"] = Insert
NormalMode.KEYMAP["a"] = Append
NormalMode.KEYMAP["I"] = InsertAtStart
NormalMode.KEYMAP["A"] = AppendAtEnd
