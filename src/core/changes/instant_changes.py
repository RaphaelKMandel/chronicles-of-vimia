from src.core.actions.changes import Delete, Backspace, ReplaceChar
from src.core.changes import Change, SingleChange, InstantChange


class DeleteChange(InstantChange):
    def __init__(self, editor):
        super().__init__(editor, Delete(editor))


class BackspaceChange(InstantChange):
    def __init__(self, editor):
        super().__init__(editor, Backspace(editor))


class ReplaceChange(SingleChange):
    def __init__(self, editor):
        super().__init__(editor, ReplaceChar(editor, self))

    def finish(self):
        self.repeat()


class RepeatLastChange:
    def __init__(self, editor):
        if Change.LAST is not None:
            self.execute()

    def execute(self):
        Change.LAST.repeat()



