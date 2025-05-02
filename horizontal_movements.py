from constants import *


class HorizontalMovement(InstantMovement):
    def execute(self):
        EDITOR.buffer.col = self.evaluate(EDITOR.buffer)


class Right(HorizontalMovement):
    def evaluate(self, buffer):
        return min(len(buffer.line) - 1, buffer.col + 1)


class Left(HorizontalMovement):
    def evaluate(self, buffer):
        return max(0, buffer.col - 1)


class Zero(HorizontalMovement):
    def evaluate(self, buffer):
        return 0


class Carrot(HorizontalMovement):
    def evaluate(self, buffer):
        for n, char in enumerate(buffer.line):
            if char != " ":
                return n

        return None


class Dollar(HorizontalMovement):
    def evaluate(self, buffer):
        return len(buffer.line) - 1


NormalMode.KEYMAP["l"] = Right
NormalMode.KEYMAP["h"] = Left
NormalMode.KEYMAP["0"] = Zero
NormalMode.KEYMAP["$"] = Dollar
NormalMode.KEYMAP["^"] = Carrot
NormalMode.KEYMAP["_"] = Carrot
