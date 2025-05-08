from classes import *
from word_parser import WordParser


class WordMovements(InstantMovement):
    def execute(self):
        col = self.evaluate(EDITOR.buffer)
        if col is not None:
            EDITOR.buffer.col = col


class StartWord(WordMovements):
    def evaluate(self, buffer):
        col = WordParser(buffer.line).next_word_start(buffer.col)
        if col is not None:
            return col

        if buffer.next_row():
            buffer.col = 0
            return WordParser(buffer.line).next_word_start(buffer.col)


class EndWord(WordMovements):
    def evaluate(self, buffer):
        col = WordParser(buffer.line).next_word_end(buffer.col)
        if col is not None:
            return col

        if buffer.next_row():
            buffer.col = 0
            return WordParser(buffer.line).next_word_end(buffer.col)


class PrevWord(WordMovements):
    def evaluate(self, buffer):
        col = WordParser(buffer.line).prev_word_start(buffer.col)
        if col is not None:
            return col

        if buffer.previous_row():
            buffer.col = len(buffer.line)
            return WordParser(buffer.line).prev_word_start(buffer._col)  # _col because col gets limited to len(line)


NormalMode.KEYMAP["w"] = StartWord
NormalMode.KEYMAP["e"] = EndWord
NormalMode.KEYMAP["b"] = PrevWord
