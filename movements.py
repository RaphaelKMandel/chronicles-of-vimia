from constants import *


class Movement:
    def __init__(self, parent):
        lines = EDITOR.buffer.lines
        row = EDITOR.buffer.row
        col = EDITOR.buffer.col
        self.execute(lines, row, col)

    def execute(self, lines, row, col):
        EDITOR.buffer.col = self.evaluate(lines, row, col)

    @staticmethod
    def evaluate(lines, row, col):
        return EDITOR.buffer.row, EDITOR.buffer.col


class Right(Movement):
    def evaluate(self, lines, row, col):
        text = lines[row]
        return min(len(text) - 1, col + 1)


class Left(Movement):
    def evaluate(self, lines, row, col):
        return max(0, col - 1)


class Zero(Movement):
    def evaluate(self, lines, row, col):
        return 0


class Carrot(Movement):
    def evaluate(self, lines, row, col):
        for n, char in enumerate(lines[row]):
            if char != " ":
                return n

        return None


class Dollar(Movement):
    def evaluate(self, lines, row, col):
        text = lines[row]
        return len(text) - 1


Normal.KEYMAP["l"] = Right
Normal.KEYMAP["h"] = Left
Normal.KEYMAP["0"] = Zero
Normal.KEYMAP["$"] = Dollar
Normal.KEYMAP["^"] = Carrot
Normal.KEYMAP["_"] = Carrot
