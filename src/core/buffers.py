from src.core.constants import *
from src.core.modes import NormalMode
from src.core.util.diffs import get_diff


class Line:
    COLORS = {
        "insert": GREEN,
        "equal": WHITE,
        "delete": RED
    }

    def __init__(self, text, target):
        self.target = target
        self.text = text
        self.words = get_diff(self.text, self.target)

    def is_solved(self):
        return self.text == self.target

    def draw(self, x, y):
        col = 0
        for op, string in self.words:
            dy = 0
            if op == "insert":
                dy = -CHAR_HEIGHT

            text_surface = FONT.render(string, True, Line.COLORS[op])
            text_rect = text_surface.get_rect(topleft=(x + CHAR_WIDTH * col, y + dy))
            SCREEN.blit(text_surface, text_rect)

            if op != "insert":
                col += len(string)


class Buffer:
    def __init__(self, game, lines, targets, name=None, x=20, y=20, credit=5):
        self.game = game
        self.name = name
        self.x, self.y = x, y
        NVIM.command("enew")
        self.buffer = NVIM.current.buffer
        self.no = self.buffer.number
        NVIM.command("setlocal undolevels=-1")
        self.buffer[:] = lines
        self.targets = targets
        NVIM.command("setlocal nomodified")
        NVIM.command("setlocal undolevels=100")
        self.credit = credit

    @property
    def lines(self):
        return NVIM.current.buffer[:]

    def get_pos(self):
        return NVIM.funcs.getpos('.')

    @property
    def row(self):
        return self.get_pos()[1]

    @property
    def col(self):
        return self.get_pos()[2]

    def width(self):
        return max([max([len(line), len(target)]) for line, target in zip(self.lines, self.targets)])

    def height(self):
        return 2 * CHAR_HEIGHT * len(self.lines)

    def get_rect(self):
        return self.x, self.y, self.width() * CHAR_WIDTH, self.height()

    def get_coord(self, row, col):
        return (
            self.y + (2 * row + 1) * CHAR_HEIGHT,
            self.x + col * CHAR_WIDTH
        )

    def draw(self):
        # Draw background
        pygame.draw.rect(SCREEN, WORD_BACKGROUND_COLOR, self.get_rect())

        # Draw text
        for n, (line, target) in enumerate(zip(self.lines, self.targets)):
            line = Line(line, target)
            line.draw(self.x, self.y + (2 * n + 1) * CHAR_HEIGHT)

        # Draw cursor

        dy = 10
        self.y += min(200, dy) / 60

    def is_solved(self):
        return all([line == target for line, target in zip(self.lines, self.targets)])

    def hit_bottom(self):
        return self.y + self.height() + BOTTOM > HEIGHT - CHAR_HEIGHT

    def test(self):
        if self.is_solved() and isinstance(self.game.mode, NormalMode):
            self.game.credit += self.credit
            self.delete()
        elif self.hit_bottom():
            self.game.debit += self.credit * 2
            self.delete()

    def delete(self):
        del self.game.buffers[self.name]
