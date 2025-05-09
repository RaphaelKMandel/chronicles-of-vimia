from classes import EDITOR, NormalMode
from motions import Down, Up


class VerticalMovement:
    def __call__(self, parent):
        self.execute()

    def __init__(self, movement):
        self.movement = movement

    def execute(self):
        if EDITOR.buffer is not None:
            new_row = self.movement.evaluate(EDITOR.buffer)
            if new_row is not None:
                EDITOR.buffer.row = new_row


class MoveDown(VerticalMovement):
    def __init__(self):
        super().__init__(Down())


class MoveUp(VerticalMovement):
    def __init__(self):
        super().__init__(Up())


NormalMode.KEYMAP["j"] = MoveDown()
NormalMode.KEYMAP["k"] = MoveUp()
