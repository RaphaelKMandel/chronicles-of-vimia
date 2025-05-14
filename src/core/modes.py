from re import match


class VimMode:
    def __init__(self, game, command):
        self.game = game
        self.command = command

    def eval(self):
        return False


class NormalMode(VimMode):
    def is_find(self):
        """
        Equals f, F, t, T, q, ', or "
        """
        return match("^[rfFtTq'\"]$", self.command)

    def is_operator(self):
        """
        Startswith d, c, y, <, >, =, and is optionally followed by i or a
        """
        return match("^[dcy<>=]([ia])?$", self.command)

    def eval(self):
        if self.is_find() or self.is_operator():
            return True


class InsertMode(VimMode):
    pass


class VisualMode(VimMode):
    def is_operator(self):
        return match("^[ia]$", self.command)

    def eval(self):
        if self.is_operator():
            return True
