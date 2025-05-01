from constants import *


class VerticalMovement(Movement):
    def execute(self, lines, row, col):
        new_row = self.evaluate(lines, row, col)
        if new_row is not None:
            EDITOR.buffer.row = new_row


class Down(VerticalMovement):
    def evaluate(self, lines, row, col):
        if row == len(lines) - 1:
            return None

        new_row = row + 1
        return new_row


class Up(VerticalMovement):
    def evaluate(self, lines, row, col):
        if row == 0:
            return None

        new_row = row - 1
        return new_row


NormalMode.KEYMAP["j"] = Down
NormalMode.KEYMAP["k"] = Up
