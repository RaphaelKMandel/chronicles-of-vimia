from re import match

from .constants import *


class VimMode:
    def __init__(self, game):
        self.game = game

    def is_pending(self, command):
        return False


class NormalMode(VimMode):
    NAME = "NORMAL"

    def draw(self, items):
        for char, x, y in items:
            pygame.draw.rect(SCREEN, CURSOR_COLOR, (x, y, CHAR_WIDTH, CHAR_HEIGHT))
            draw_text(char, x, y, CURSOR_TEXT_COLOR)

    def is_find(self, command):
        """
        Equals f, F, t, T, q, ', or "
        """
        return match("^[rfFtTq'\"]$", command)

    def is_operator(self, command):
        """
        Startswith d, c, y, <, >, =, and is optionally followed by i or a
        """
        return match("^[dcy<>=]([iafFtT])?$", command)

    def is_command(self, command):
        return match("^:.*[^\u000D]$|^:$", command)

    def is_pending(self, command):
        if self.is_find(command) or self.is_operator(command) or self.is_command(command):
            return True


class LostMode(NormalMode):
    NAME = "GAME OVER"


class InsertMode(VimMode):
    NAME = "-- INSERT --"

    def draw(self, items):
        for text, x, y in items:
            pygame.draw.rect(SCREEN, CURSOR_COLOR, (x, y, CHAR_WIDTH // 4, CHAR_HEIGHT))


class VisualMode(VimMode):
    NAME = "VISUAL"

    def is_operator(self, command):
        return match("^[ia]$", command)

    def is_pending(self, command):
        if self.is_operator(command):
            return True
