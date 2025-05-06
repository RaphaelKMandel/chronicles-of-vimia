from constants import *

WORD_BOUNDARIES = "{}[](),.'\"-+:/"

# Test {}[](),.'"


class WordMovement(InstantMovement):
    def execute(self):
        col = self.evaluate(EDITOR.buffer)
        if col:
            EDITOR.buffer.col = col

    def evaluate(self, buffer):
        return self.find_next_word(buffer.line, buffer.col)

    def next_line(self):
        if EDITOR.buffer.next_row():
            return self.find_next_word(EDITOR.buffer.line, 0)

    def find_next_blank(self, line, col):
        if col == len(line) - 1:
            return self.next_line()

        for col, char in enumerate(line[col + 1:], start=col + 1):
            if char == " ":
                return self.find_next_word_from_blank(line, col + 1)
        else:
            return self.next_line()

    def find_next_word(self, line, col):
        if col >= len(line):
            return self.next_line()

        for col, char in enumerate(line[col + 1:], start=col + 1):
            if char == " ":
                return self.find_next_word_from_blank(line, col + 1)

            if char in WORD_BOUNDARIES:
                return col

        else:
            return self.next_line()

    def find_next_word_from_blank(self, line, col):
        for col, char in enumerate(line[col:], start=col):
            if char != " ":
                return col
        else:
            return self.next_line()


class EndWord(InstantMovement):
    pass


NormalMode.KEYMAP["w"] = WordMovement
