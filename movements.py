from constants import *


class Movement:
    pass


class Right:
    def __init__(self, game):
        game.buffer.col = min(len(game.buffer.text), game.buffer.col+1)

NormalMode.KEYMAP["l"] = Right


class Left:
    def __init__(self, game):
        game.buffer.col = max(0, game.buffer.col-1)

NormalMode.KEYMAP["h"] = Left

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