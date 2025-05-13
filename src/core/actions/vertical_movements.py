from src.core.actions import InstantAction
from src.core.motions import Down, Up


class VerticalMovement(InstantAction):
    def execute(self):
        if self.editor.buffer is not None:
            new_row = self.motion.evaluate(self.editor.buffer)
            if new_row is not None:
                self.editor.buffer.row = new_row


class MoveDown(VerticalMovement):
    def __init__(self, editor):
        super().__init__(editor, Down(editor))


class MoveUp(VerticalMovement):
    def __init__(self, editor):
        super().__init__(editor, Up(editor))



