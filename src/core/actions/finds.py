from src.core.actions import Action
from src.core.motions import Find


class FindMovement(Action):
    def __init__(self, editor, motion):
        super().__init__(editor, motion)

    def finish(self):
        self.execute()

    def execute(self, reversed=False):
        new_col = self.motion.evaluate(self.editor.buffer, reversed=reversed)
        if new_col is not None:
            self.editor.buffer.col = new_col


class FindForwardMovement(FindMovement):
    def __init__(self, editor):
        super().__init__(editor, Find(editor, self, forward=True, offset=0))


class FindBackwardMovement(FindMovement):
    def __init__(self, editor):
        super().__init__(editor, Find(editor, self, forward=False, offset=0))


class FindForwardToMovement(FindMovement):
    def __init__(self, editor):
        super().__init__(editor, Find(editor, self, forward=True, offset=1))


class FindBackwardToMovement(FindMovement):
    def __init__(self, editor):
        super().__init__(editor, Find(editor, self, forward=False, offset=1))


class RepeatFindForwardMovement:
    def __init__(self, editor):
        if Find.LAST is not None:
            FindMovement(editor, Find.LAST).execute(reversed=False)


class RepeatFindBackwardMovement:
    def __init__(self, editor):
        if Find.LAST is not None:
            FindMovement(editor, Find.LAST).execute(reversed=True)
