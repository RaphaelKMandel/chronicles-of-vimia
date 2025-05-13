from src.core.changes import Change
from src.core.actions.changes import Delete
from src.core.actions.insert_mode_actions import EnterInsertMode, LeaveInsertMode
from src.core.actions.horizontal_movements import MoveRight, MoveCarrot, MoveDollar


class InsertModeChange(Change):
    def __init__(self, editor):
        super().__init__(editor)
        self.add_and_execute_action(EnterInsertMode(editor, self))

    def finish(self, actions):
        for action in actions:
            self.actions.append(action)  # Do not use add_action(), do not want to execute the action again

        self.add_and_execute_action(LeaveInsertMode(self.editor))


class InsertChange(InsertModeChange):
    def __init__(self, editor):
        super().__init__(editor)
        self.register()


class SubsChange(Change):
    def __init__(self, editor):
        super().__init__(editor)
        self.register()
        self.add_and_execute_action(Delete(editor))
        self.actions.append(InsertModeChange(editor))


class AppendChange(InsertModeChange):
    def __init__(self, editor):
        super().__init__(editor)
        self.register()
        self.actions.append(MoveRight(editor))


class InsertAtStartChange(InsertModeChange):
    def __init__(self, editor):
        super().__init__(editor)
        self.register()
        self.actions.append(MoveCarrot(editor))


class AppendAtEndChange(InsertModeChange):
    def __init__(self, editor):
        super().__init__(editor)
        self.register()
        self.actions.append(MoveDollar(editor))
