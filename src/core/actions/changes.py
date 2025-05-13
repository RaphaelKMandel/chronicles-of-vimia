from src.core.actions import Action
from src.core.motions import Char


class Delete(Action):
    def execute(self):
        buffer = self.editor.buffer
        line = buffer.line
        new_line = line[:buffer.col]
        if buffer.col < len(line) - 1:
            new_line += line[buffer.col + 1:]

        buffer.line = new_line
        buffer.col = buffer.col  # Needed to reset column to current column


class Backspace(Action):
    def execute(self):
        buffer = self.editor.buffer
        line = buffer.line
        buffer.line = line[:buffer.col - 1] + line[buffer.col:]
        buffer.col -= 1


class InsertChar(Action):
    def __init__(self, editor, char):
        self.char = char
        super().__init__(editor)

    def execute(self):
        line, col = self.editor.buffer.line, self.editor.buffer.col
        self.editor.buffer.line = line[:col] + self.char + line[col:]
        self.editor.buffer.col += 1


class ReplaceChar(Action):
    def __init__(self, editor, parent):
        super().__init__(editor)
        self.parent = parent
        self.motion = Char(editor, self)

    def finish(self):
        self.char = self.motion.char
        self.parent.finish()

    def execute(self):
        if self.char is not None:
            col = self.editor.buffer.col
            line = self.editor.buffer.line
            self.editor.buffer.line = line[:col] + self.char + line[col + 1:]
