from constants import *


class VerticalMovement(Movement):
    def execute(self):
        new_row = self.evaluate(EDITOR.buffer)
        if new_row is not None:
            EDITOR.buffer.row = new_row


class Down(VerticalMovement):
    def evaluate(self, buffer):
        if buffer.row == len(buffer.lines) - 1:
            return None

        return buffer.row + 1


class Up(VerticalMovement):
    def evaluate(self, buffer):
        if buffer.row == 0:
            return None

        return buffer.row - 1


NormalMode.KEYMAP["j"] = Down
NormalMode.KEYMAP["k"] = Up
