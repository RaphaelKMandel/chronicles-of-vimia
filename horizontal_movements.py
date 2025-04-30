from constants import *


class HorizontalMovement(Movement):
    def execute(self, lines, row, col):
        EDITOR.buffer.col = self.evaluate(lines, row, col)


class Right(HorizontalMovement):
    def evaluate(self, lines, row, col):
        text = lines[row]
        return min(len(text) - 1, col + 1)


class Left(HorizontalMovement):
    def evaluate(self, lines, row, col):
        return max(0, col - 1)


class Zero(HorizontalMovement):
    def evaluate(self, lines, row, col):
        return 0


class Carrot(HorizontalMovement):
    def evaluate(self, lines, row, col):
        for n, char in enumerate(lines[row]):
            if char != " ":
                return n

        return None


class Dollar(HorizontalMovement):
    def evaluate(self, lines, row, col):
        text = lines[row]
        return len(text) - 1


Normal.KEYMAP["l"] = Right
Normal.KEYMAP["h"] = Left
Normal.KEYMAP["0"] = Zero
Normal.KEYMAP["$"] = Dollar
Normal.KEYMAP["^"] = Carrot
Normal.KEYMAP["_"] = Carrot
