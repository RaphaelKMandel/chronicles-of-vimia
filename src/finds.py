from classes import *
from motions import ForwardFind, BackwardFind


class FindState(NormalMode):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def handle_input(self, event):
        self.parent.finish(event.unicode)


class Find:
    LAST_SEARCH = None

    def __call__(self):
        Find.LAST_SEARCH = self
        self.state = FindState(self)

    def __init__(self, forward, offset):
        self.char = ""
        self.forward = forward
        self.offset = offset

    def finish(self, char):
        self.char = char
        self.execute()
        EDITOR.state = EDITOR.normal

    def execute(self, reversed=False):
        forward = self.forward if not reversed else not self.forward
        if forward:
            new_col = ForwardFind(self.char, self.offset).evaluate(EDITOR.buffer)
        else:
            new_col = BackwardFind(self.char, self.offset).evaluate(EDITOR.buffer)

        if new_col is not None:
            EDITOR.buffer.col = new_col


class FindForward(Find):
    def __init__(self):
        super().__init__(forward=True, offset=0)


class FindBackward(Find):
    def __init__(self):
        super().__init__(forward=False, offset=0)


class FindForwardTo(Find):
    def __init__(self):
        super().__init__(forward=True, offset=1)


class FindBackwardTo(Find):
    def __init__(self):
        super().__init__(forward=False, offset=1)


class RepeatFindForward:
    def __call__(self):
        if Find.LAST_SEARCH is not None:
            Find.LAST_SEARCH.execute(reversed=False)


class RepeatFindBackward:
    def __call__(self):
        if Find.LAST_SEARCH is not None:
            Find.LAST_SEARCH.execute(reversed=True)


NormalMode.KEYMAP["f"] = FindForward()
NormalMode.KEYMAP["F"] = FindBackward()
NormalMode.KEYMAP["t"] = FindForwardTo()
NormalMode.KEYMAP["T"] = FindBackwardTo()
NormalMode.KEYMAP[";"] = RepeatFindForward()
NormalMode.KEYMAP[","] = RepeatFindBackward()

if __name__ == "__main__":
    pass
