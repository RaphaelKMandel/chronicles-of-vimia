from classes import EDITOR, NormalMode, InstantMovement
from motions import Left, Right, Zero, Carrot, Dollar, StartWord, EndWord, PrevWord


class HorizontalMovement(InstantMovement):
    def execute(self):
        if EDITOR.buffer is not None:
            new_col = self.movement.evaluate(EDITOR.buffer)
            if new_col is not None:
                EDITOR.buffer.col = new_col


class MoveLeft(HorizontalMovement):
    def __init__(self):
        super().__init__(Left())


class MoveRight(HorizontalMovement):
    def __init__(self):
        super().__init__(Right())


class MoveZero(HorizontalMovement):
    def __init__(self):
        super().__init__(Zero())


class MoveCarrot(HorizontalMovement):
    def __init__(self):
        super().__init__(Carrot())


class MoveDollar(HorizontalMovement):
    def __init__(self):
        super().__init__(Dollar())


class MoveStartWord(HorizontalMovement):
    def __init__(self):
        super().__init__(StartWord())


class MoveEndWord(HorizontalMovement):
    def __init__(self):
        super().__init__(EndWord())


class MovePrevWord(HorizontalMovement):
    def __init__(self):
        super().__init__(PrevWord())


NormalMode.KEYMAP["h"] = MoveLeft()
NormalMode.KEYMAP["l"] = MoveRight()
NormalMode.KEYMAP["0"] = MoveZero()
NormalMode.KEYMAP["^"] = MoveCarrot()
NormalMode.KEYMAP["_"] = MoveCarrot()
NormalMode.KEYMAP["$"] = MoveDollar()
NormalMode.KEYMAP["w"] = MoveStartWord()
NormalMode.KEYMAP["e"] = MoveEndWord()
NormalMode.KEYMAP["b"] = MovePrevWord()
