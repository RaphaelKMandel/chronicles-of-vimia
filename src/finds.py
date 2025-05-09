from classes import *
from motions import Find


class FindState(NormalMode):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def handle_input(self, event):
        self.finish(event.unicode)

    def finish(self, char):
        EDITOR.pop()
        self.parent.finish(char)


class FindMotionBuilder:
    def __init__(self, parent, forward, offset):
        self.parent = parent
        self.forward = forward
        self.offset = offset
        self.state = FindState(self)

    def finish(self, char):
        if char.isprintable():
            motion = Find(char, self.forward, self.offset)
            self.parent.finish(motion)


class FindMotion:
    def __init__(self, parent, forward, offset):
        self.parent = parent
        self.motion = None
        FindMotionBuilder(self, forward=forward, offset=offset)

    def finish(self, motion):
        FindMovement.LAST = FindMovement(motion)
        self.motion = motion
        self.parent.finish()

    def evaluate(self, buffer, reversed=False):
        return self.motion.evaluate(buffer, reversed=reversed)


class FindForward(FindMotion):
    def __init__(self, parent):
        super().__init__(parent, forward=True, offset=0)


class FindBackward(FindMotion):
    def __init__(self, parent):
        super().__init__(parent, forward=False, offset=0)


class FindForwardTo(FindMotion):
    def __init__(self, parent):
        super().__init__(parent, forward=True, offset=1)


class FindBackwardTo(FindMotion):
    def __init__(self, parent):
        super().__init__(parent, forward=False, offset=1)


class FindMovement:
    LAST = None

    def __init__(self, motion):
        self.motion = motion

    def finish(self):
        self.execute()

    def execute(self, reversed=False):
        new_col = self.motion.evaluate(EDITOR.buffer, reversed=reversed)
        if new_col is not None:
            EDITOR.buffer.col = new_col


class FindForwardMovement(FindMovement):
    def __init__(self):
        super().__init__(FindForward(self))


class FindBackwardMovement(FindMovement):
    def __init__(self):
        super().__init__(FindBackward(self))


class FindForwardToMovement(FindMovement):
    def __init__(self):
        super().__init__(FindForwardTo(self))


class FindBackwardToMovement(FindMovement):
    def __init__(self):
        super().__init__(FindBackwardTo(self))


class RepeatFindForwardMovement:
    def __init__(self):
        if FindMovement.LAST is not None:
            FindMovement.LAST.execute(reversed=False)


class RepeatFindBackwardMovement:
    def __init__(self):
        if FindMovement.LAST is not None:
            FindMovement.LAST.execute(reversed=True)


NormalMode.KEYMAP["f"] = FindForwardMovement
NormalMode.KEYMAP["F"] = FindBackwardMovement
NormalMode.KEYMAP["t"] = FindForwardToMovement
NormalMode.KEYMAP["T"] = FindBackwardToMovement
NormalMode.KEYMAP[";"] = RepeatFindForwardMovement
NormalMode.KEYMAP[","] = RepeatFindBackwardMovement
