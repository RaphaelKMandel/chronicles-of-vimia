from src.core.states import NormalMode
from src.core.actions import InstantAction


class BufferMemento:
    """Used to save state for undo/redo."""

    def __init__(self, buffer):
        self.lines = [line.text for line in buffer.lines]
        self.row = buffer.row
        self.col = buffer.col

    def restore(self, buffer):
        for line, text in zip(buffer.lines, self.lines):
            line.text = text

        buffer.row, buffer.col = self.row, self.col


class Undo(InstantAction):
    def execute(self):
        if self.editor.buffer.undo_list:
            self.editor.buffer.redo_list.append(BufferMemento(self.editor.buffer))
            buffer_state = self.editor.buffer.undo_list.pop()
            buffer_state.restore(self.editor.buffer)


class Redo(InstantAction):
    def execute(self):
        if self.editor.buffer.redo_list:
            self.editor.buffer.undo_list.append(BufferMemento(self.editor.buffer))
            buffer_state = self.editor.buffer.redo_list.pop()
            buffer_state.restore(self.editor.buffer)
