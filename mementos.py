from constants import *


class Undo(Child):
    def __init__(self, parent):
        super().__init__(parent)
        self.execute()

    def execute(self):
        if EDITOR.buffer.undo_list:
            EDITOR.buffer.redo_list.append(EDITOR.buffer.copy())
            buffer = EDITOR.buffer.undo_list.pop()
            EDITOR.buffer.lines = buffer.lines
            EDITOR.buffer.row, EDITOR.buffer.col = buffer.row, buffer.col


class Redo(Child):
    def __init__(self, parent):
        super().__init__(parent)
        self.execute()

    def execute(self):
        if EDITOR.buffer.redo_list:
            EDITOR.buffer.undo_list.append(EDITOR.buffer.copy())
            buffer = EDITOR.buffer.redo_list.pop()
            EDITOR.buffer.lines = buffer.lines
            EDITOR.buffer.row, EDITOR.buffer.col = buffer.row, buffer.col


NormalMode.KEYMAP["u"] = Undo
NormalMode.KEYMAP["U"] = Redo  # My preferred keybind
NormalMode.KEYMAP["\x12"] = Redo
