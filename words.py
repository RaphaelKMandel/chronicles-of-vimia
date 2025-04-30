# class WordMovement(Movement):
#     def __init__(self, game):
#         EDITOR = game
#         self.buffer = game.buffer
#         self.text = game.buffer.text
#         self.col = game.buffer.col
#         EDITOR.buffer.col = self.find_next_word()
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
