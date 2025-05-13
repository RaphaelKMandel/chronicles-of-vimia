class Action:
    def __init__(self, editor, motion=None):
        self.editor = editor
        self.motion = motion

    def execute(self):
        pass


class InstantAction(Action):
    def __init__(self, editor, motion=None):
        super().__init__(editor, motion)
        self.execute()
