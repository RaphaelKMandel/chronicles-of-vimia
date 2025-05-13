from src.core.states import CharMode
from src.core.util.word_parser import WordParser


class Motion:
    def __init__(self, editor):
        self.editor = editor

    def evaluate(self, buffer):
        raise NotImplementedError()


class Right(Motion):
    def evaluate(self, buffer):
        max_col = buffer.editor.state.max_col()
        return min(max_col, buffer._col + 1)


class Left(Motion):
    def evaluate(self, buffer):
        return max(0, buffer.col - 1)


class Zero(Motion):
    def evaluate(self, buffer):
        return 0


class Carrot(Motion):
    def evaluate(self, buffer):
        for n, char in enumerate(buffer.line):
            if char != " ":
                return n

        return None


class Dollar(Motion):
    def evaluate(self, buffer):
        return buffer.editor.state.max_col()


class Down(Motion):
    def evaluate(self, buffer):
        if buffer.row == len(buffer.lines) - 1:
            return None

        return buffer.row + 1


class Up(Motion):
    def evaluate(self, buffer):
        if buffer.row == 0:
            return None

        return buffer.row - 1


class Char(Motion):
    def __init__(self, editor, parent):
        super().__init__(editor)
        self.parent = parent
        self.char = None
        CharMode(editor, self)

    def finish(self, char):
        if char.isprintable():
            self.char = char
            self.parent.finish()

    def evaluate(self, buffer):
        pass


class Find(Char):
    LAST = None

    def __init__(self, editor, parent, forward, offset):
        self.forward = forward
        self.offset = offset
        super().__init__(editor, parent)

    def finish(self, char):
        Find.LAST = self
        super().finish(char)

    def evaluate(self, buffer, reversed=False):
        forward = self.forward if not reversed else not self.forward
        if forward:
            return self.forward_find(buffer)
        else:
            return self.backward_find(buffer)

    def forward_find(self, buffer):
        for col, char in enumerate(buffer.line[buffer.col + 1 + self.offset:], start=buffer.col + 1 + self.offset):
            if char == self.char:
                return col - self.offset

        return None

    def backward_find(self, buffer):
        for col, char in zip(reversed(range(buffer.col - self.offset)),
                             reversed(buffer.line[:buffer.col - self.offset])):
            if char == self.char:
                return col + self.offset

        return None


class StartWord(Motion):
    def evaluate(self, buffer):
        col = WordParser(buffer.line).next_word_start(buffer.col)
        if col is not None:
            return col

        if buffer.next_row():
            buffer.col = 0
            return WordParser(buffer.line).next_word_start(buffer.col)


class EndWord(Motion):
    def evaluate(self, buffer):
        col = WordParser(buffer.line).next_word_end(buffer.col)
        if col is not None:
            return col

        if buffer.next_row():
            buffer.col = 0
            return WordParser(buffer.line).next_word_end(buffer.col)


class PrevWord(Motion):
    def evaluate(self, buffer):
        col = WordParser(buffer.line).prev_word_start(buffer.col)
        if col is not None:
            return col

        if buffer.previous_row():
            buffer.col = len(buffer.line)
            return WordParser(buffer.line).prev_word_start(buffer._col)  # _col because col gets limited to len(line)
