from re import match

from .constants import *


class VimMode:
    def __init__(self, game):
        self.game = game

    def is_pending(self, command):
        return False


class NormalMode(VimMode):
    NAME = "NORMAL"
    COUNT = "([1-9][0-9]*)"

    def draw(self, items):
        for char, x, y in items:
            pygame.draw.rect(SCREEN, CURSOR_COLOR, (x, y, CHAR_WIDTH, CHAR_HEIGHT))
            draw_text(char, x, y, CURSOR_TEXT_COLOR)

    def is_count(self, command):
        return match(f"^{NormalMode.COUNT}$", command)

    def is_find(self, command):
        return match(f"^({NormalMode.COUNT})?[fFtT]$", command)

    def is_char(self, command):
        return match("^[rq@'\"]$", command)

    def is_operator(self, command):
        return match(f"^[dcy<>=]({NormalMode.COUNT})?([iafFtT])?$", command)

    def is_command(self, command):
        return match("^:.*[^\u000D]$|^:$", command)

    def is_pending(self, command):
        if any([self.is_count(command),
                self.is_find(command),
                self.is_char(command),
                self.is_operator(command),
                self.is_command(command)
                ]):
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
