from constants import *


class Movement:
    def __init__(self, game):
        self.game = game
        game.buffer.col = self.compute_move()

    def compute_move(self):
        return self.game.buffer.col


class Right(Movement):
    def compute_move(self):
        return min(len(self.game.buffer.text) - 1, self.game.buffer.col + 1)


NormalMode.KEYMAP["l"] = Right


class Left(Movement):
    def compute_move(self):
        return max(0, self.game.buffer.col - 1)


NormalMode.KEYMAP["h"] = Left


class Zero(Movement):
    def compute_move(self):
        return 0


NormalMode.KEYMAP["0"] = Zero


class Dollar(Movement):
    def compute_move(self):
        return len(self.game.buffer.text) - 1


NormalMode.KEYMAP["$"] = Dollar


class FindForward(State):
    def __init__(self, game):
        super().__init__(game)
        self.char = ""

    def handle_input(self, event):
        print("Find Forward", self.char, event)
        self.char = event.unicode
        self.game.buffer.col = self.compute_move()
        self.game.state = NormalMode(self.game)

    def compute_move(self):
        if self.char in self.game.buffer.text[self.game.buffer.col+1:]:
            return self.game.buffer.col + 1 + self.game.buffer.text[self.game.buffer.col+1:].index(self.char)

        return self.game.buffer.col


NormalMode.KEYMAP["f"] = FindForward

# class WordMovement(Movement):
#     def __init__(self, game):
#         self.game = game
#         self.buffer = game.buffer
#         self.text = game.buffer.text
#         self.col = game.buffer.col
#         self.game.buffer.col = self.find_next_word()
#
#     def find_next_word(self):
#         col = self.find_next_boundary()
#
#
#         for end, char in enumerate(text[col:], start=col):
#             if char in {" ", "["}:
#                 return end + 1
#
#     def find_next_boundary(self):
#         for col, char in enumerate(self.text[self.col:], start=self.col):
#             if char == " ":
#                 return col
#
#
# NormalMode.KEYMAP["w"] = WordMovement
