from constants import *
from horizontal_movements import Carrot, Dollar


class Insert(Action):
    def __init__(self, parent):
        super().__init__(parent)
        InsertMode(parent)


class Append(Action):
    def __init__(self, parent):
        super().__init__(parent)
        EDITOR.buffer.col += 1
        InsertMode(parent)


class InsertAtStart(Action):
    def __init__(self, parent):
        super().__init__(parent)
        EDITOR.buffer.col = Carrot(parent).evaluate(EDITOR.buffer)
        Insert(parent)


class AppendAtEnd(Action):
    def __init__(self, parent):
        super().__init__(parent)
        EDITOR.buffer.col = Dollar(parent).evaluate(EDITOR.buffer)
        Append(parent)


NormalMode.KEYMAP["i"] = Insert
NormalMode.KEYMAP["a"] = Append
NormalMode.KEYMAP["I"] = InsertAtStart
NormalMode.KEYMAP["A"] = AppendAtEnd
