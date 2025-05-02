from constants import *


class FindState(State):
    NAME = NormalMode.NAME

    def __init__(self, parent, forward=True):
        super().__init__(parent)
        self.forward = forward

    def handle_input(self, event):
        self.parent.char = event.unicode
        self.deactivate()


class Find(Movement):
    def __init__(self, parent, forward, offset):
        super().__init__(parent)
        self.char = ""
        self.forward = forward
        self.offset = offset
        self.state = FindState(self)

    def activate(self):
        EDITOR.last_search = self
        self.execute()
        self.deactivate()

    def deactivate(self):
        self.parent.activate()

    def execute(self, reversed=False):
        forward = self.forward if not reversed else not self.forward
        if forward:
            new_col = self.forward_search(EDITOR.buffer)
        else:
            new_col = self.backward_search(EDITOR.buffer)

        if new_col is not None:
            EDITOR.buffer.col = new_col

    def forward_search(self, buffer):
        for col, char in enumerate(buffer.line[buffer.col + 1 + self.offset:], start=buffer.col + 1 + self.offset):
            if char == self.char:
                return col - self.offset

        return None

    def backward_search(self, buffer):
        for col, char in zip(reversed(range(buffer.col - self.offset)),
                             reversed(buffer.line[:buffer.col - self.offset])):
            if char == self.char:
                return col + self.offset

        return None


class FindForward(Find):
    def __init__(self, parent):
        super().__init__(parent, forward=True, offset=0)


class FindBackward(Find):
    def __init__(self, parent):
        super().__init__(parent, forward=False, offset=0)


class FindForwardTo(Find):
    def __init__(self, parent):
        super().__init__(parent, forward=True, offset=1)


class FindBackwardTo(Find):
    def __init__(self, parent):
        super().__init__(parent, forward=False, offset=1)


class RepeatFindForward:
    def __init__(self, parent):
        EDITOR.last_search.execute(reversed=False)


class RepeatFindBackward:
    def __init__(self, parent):
        EDITOR.last_search.execute(reversed=True)


NormalMode.KEYMAP["f"] = FindForward
NormalMode.KEYMAP["F"] = FindBackward
NormalMode.KEYMAP["t"] = FindForwardTo
NormalMode.KEYMAP["T"] = FindBackwardTo
NormalMode.KEYMAP[";"] = RepeatFindForward
NormalMode.KEYMAP[","] = RepeatFindBackward

if __name__ == "__main__":
    pass
