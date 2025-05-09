from classes import *


class Undo:
    def __call__(self):
        self.execute()

    def execute(self):
        if EDITOR.buffer.undo_list:
            EDITOR.buffer.redo_list.append(BufferMemento(EDITOR.buffer))
            buffer_state = EDITOR.buffer.undo_list.pop()
            buffer_state.restore(EDITOR.buffer)


class Redo:
    def __call__(self):
        self.execute()

    def execute(self):
        if EDITOR.buffer.redo_list:
            EDITOR.buffer.undo_list.append(BufferMemento(EDITOR.buffer))
            buffer_state = EDITOR.buffer.redo_list.pop()
            buffer_state.restore(EDITOR.buffer)


NormalMode.KEYMAP["u"] = Undo()
NormalMode.KEYMAP["U"] = Redo()  # My preferred keybind
NormalMode.KEYMAP["\x12"] = Redo()
