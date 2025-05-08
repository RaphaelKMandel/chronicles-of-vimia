from classes import *


class Action(Child):
    def full_execute(self):
        self.register()
        self.execute()

    def register(self):
        EDITOR.last_action = self
        EDITOR.buffer.redo_list = []
        EDITOR.buffer.undo_list.append(BufferMemento(EDITOR.buffer))

    def execute(self):
        pass


class InstantAction(Action):
    def __init__(self, parent):
        super().__init__(parent)
        self.full_execute()


class CompoundAction(Action):
    def __init__(self, parent):
        super().__init__(parent)
        self.actions = []

    def execute(self):
        for action in self.actions:
            action.execute()
