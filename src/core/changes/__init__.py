from src.core.actions.mementos import BufferMemento


class Change:
    LAST = None

    def __init__(self, editor):
        self.editor = editor
        self.actions = []

    def add_and_execute_action(self, action):
        self.actions.append(action)
        action.execute()

    def repeat(self):
        self.register()
        self.execute()

    def register(self):
        Change.LAST = self
        self.editor.buffer.redo_list = []
        self.editor.buffer.undo_list.append(BufferMemento(self.editor.buffer))

    def execute(self):
        for action in self.actions:
            action.execute()


class SingleChange(Change):
    def __init__(self, editor, action):
        super().__init__(editor)
        self.register()
        self.actions.append(action)


class InstantChange(SingleChange):
    def __init__(self, editor, action):
        super().__init__(editor, action)
        self.execute()