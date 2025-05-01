from constants import *






class Insert:
    def __init__(self, parent):
        self.parent = parent
        InsertMode(parent)


class Append:
    def __init__(self, parent):
        self.parent = parent
        EDITOR.buffer.col += 1
        InsertMode(parent)


NormalMode.KEYMAP["i"] = Insert
NormalMode.KEYMAP["a"] = Append
