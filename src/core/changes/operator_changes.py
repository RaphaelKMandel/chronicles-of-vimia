from src.core.states import *
from src.core.changes import Change
from src.core.changes.inserts import InsertModeChange
from src.core.motions import StartWord, EndWord, PrevWord, Find


class OperatorMode(NormalMode):
    KEYMAP = {}

    def __init__(self, editor, parent):
        super().__init__(editor)
        self.parent = parent
        self.motion = None

    def handle_input(self, event):
        command = self.get_command(event)
        if command is not None:
            command(self.editor, self)

    def finish(self, motion):
        self.editor.pop()
        self.parent.finish(motion)


class OperatorAction(Change):
    def __init__(self, editor):
        super().__init__(editor)
        self.register()
        self.motion = None
        OperatorMode(editor, self)

    def finish(self, motion):
        self.motion = motion
        self.execute()


class DeleteOperator(OperatorAction):
    def execute(self):
        buffer = self.editor.buffer
        row, col = buffer.row, buffer.col
        new_row, new_col = self.motion.evaluate(buffer)
        if row == new_row and new_col is not None:
            if col > new_col:
                col, new_col = new_col, col

            new_col += 1
            line = buffer.line
            buffer.line = line[:col] + line[new_col:]
            buffer.col = col


class ChangeOperator(DeleteOperator):
    def __init__(self, editor):
        super().__init__(editor)
        self.insert = None

    def finish(self, motion):
        self.motion = motion
        super().execute()
        self.insert = InsertModeChange(self.editor)

    def execute(self):
        super().execute()
        self.insert.execute()


class FindAction:
    def __init__(self, editor, parent, motion):
        self.editor = editor
        self.parent = parent
        self.motion = motion

    def finish(self):
        self.parent.finish(self)

    def evaluate(self, buffer):
        col = self.motion.evaluate(buffer)
        return buffer.row, col


class FindForwardAction(FindAction):
    def __init__(self, editor, parent):
        super().__init__(editor, parent, Find(editor, self, forward=True, offset=0))


class FindBackwardAction(FindAction):
    def __init__(self, editor, parent):
        super().__init__(editor, parent, Find(editor, self, forward=False, offset=0))


class FindForwardToAction(FindAction):
    def __init__(self, editor, parent):
        super().__init__(editor, parent, Find(editor, self, forward=True, offset=1))


class FindBackwardToAction(FindAction):
    def __init__(self, editor, parent):
        super().__init__(editor, parent, Find(editor, self, forward=False, offset=1))


class StartWordAction:
    def __init__(self, editor, parent):
        self.editor = editor
        self.parent = parent
        self.motion = StartWord(editor)
        self.parent.finish(self)

    def evaluate(self, buffer):
        col = self.motion.evaluate(buffer)
        if col is not None:
            col -= 1
        return buffer.row, col


class EndWordAction:
    def __init__(self, editor, parent):
        self.editor = editor
        self.parent = parent
        self.motion = EndWord(self.editor)
        self.parent.finish(self)

    def evaluate(self, buffer):
        col = self.motion.evaluate(buffer)
        return buffer.row, col


class PrevWordAction:
    def __init__(self, editor, parent):
        self.editor = editor
        self.parent = parent
        self.motion = PrevWord(editor)
        self.parent.finish(self)

    def evaluate(self, buffer):
        col = self.motion.evaluate(buffer)
        return buffer.row, col
