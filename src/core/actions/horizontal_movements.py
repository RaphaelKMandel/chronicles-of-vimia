from src.core.actions import InstantAction
from src.core.motions import Left, Right, Zero, Carrot, Dollar, StartWord, EndWord, PrevWord


class HorizontalMovement(InstantAction):
    def execute(self):
        if self.editor.buffer is not None:
            new_col = self.motion.evaluate(self.editor.buffer)
            if new_col is not None:
                self.editor.buffer.col = new_col


class MoveLeft(HorizontalMovement):
    def __init__(self, editor):
        super().__init__(editor, Left(editor))


class MoveRight(HorizontalMovement):
    def __init__(self, editor):
        super().__init__(editor, Right(editor))


class MoveZero(HorizontalMovement):
    def __init__(self, editor):
        super().__init__(editor, Zero(editor))


class MoveCarrot(HorizontalMovement):
    def __init__(self, editor):
        super().__init__(editor, Carrot(editor))


class MoveDollar(HorizontalMovement):
    def __init__(self, editor):
        super().__init__(editor, Dollar(editor))


class MoveStartWord(HorizontalMovement):
    def __init__(self, editor):
        super().__init__(editor, StartWord(editor))


class MoveEndWord(HorizontalMovement):
    def __init__(self, editor):
        super().__init__(editor, EndWord(editor))


class MovePrevWord(HorizontalMovement):
    def __init__(self, editor):
        super().__init__(editor, PrevWord(editor))



