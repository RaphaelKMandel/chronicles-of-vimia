from classes import *
from motions import Find


class FindMovement:
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
        super().__init__(Find(self, forward=True, offset=0))


class FindBackwardMovement(FindMovement):
    def __init__(self):
        super().__init__(Find(self, forward=False, offset=0))


class FindForwardToMovement(FindMovement):
    def __init__(self):
        super().__init__(Find(self, forward=True, offset=1))


class FindBackwardToMovement(FindMovement):
    def __init__(self):
        super().__init__(Find(self, forward=False, offset=1))


class RepeatFindForwardMovement:
    def __init__(self):
        if Find.LAST is not None:
            FindMovement(Find.LAST).execute(reversed=False)


class RepeatFindBackwardMovement:
    def __init__(self):
        if Find.LAST is not None:
            FindMovement(Find.LAST).execute(reversed=True)


NormalMode.KEYMAP["f"] = FindForwardMovement
NormalMode.KEYMAP["F"] = FindBackwardMovement
NormalMode.KEYMAP["t"] = FindForwardToMovement
NormalMode.KEYMAP["T"] = FindBackwardToMovement
NormalMode.KEYMAP[";"] = RepeatFindForwardMovement
NormalMode.KEYMAP[","] = RepeatFindBackwardMovement
