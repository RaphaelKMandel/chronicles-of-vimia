from src.core.actions import Action
from src.core.states.insert_states import InsertMode


class EnterInsertMode(Action):
    def __init__(self, editor, parent):
        super().__init__(editor)
        self.parent = parent
        self.state = None

    def execute(self):
        self.state = InsertMode(self.editor, self)

    def finish(self):
        if self.state is not None:
            self.parent.finish(self.state.actions)


class LeaveInsertMode(Action):
    def execute(self):
        self.editor.pop()
