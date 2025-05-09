from classes import *


class Action(Child):
    LAST_ACTION = None

    def full_execute(self):
        self.register()
        self.execute()

    def register(self):
        Action.LAST_ACTION = self
        EDITOR.buffer.redo_list = []
        EDITOR.buffer.undo_list.append(BufferMemento(EDITOR.buffer))

    def execute(self):
        pass


class InstantAction(Action):
    def __call__(self, parent):
        self.full_execute()

    def __init__(self):
        pass


class CompoundAction(Action):
    def __init__(self):
        self.actions = []

    def execute(self):
        for action in self.actions:
            action.execute()
