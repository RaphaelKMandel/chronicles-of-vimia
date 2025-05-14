from src.core.constants import *
from src.core.modes import NormalMode
from src.core.buffers import Buffer
from src.core.diffs import get_diff


class LineDrawer:
    COLORS = {
        "insert": GREEN,
        "equal": WHITE,
        "delete": RED
    }

    def __init__(self, text, target):
        self.target = target
        self.text = text
        self.words = get_diff(self.text, self.target)

    def draw(self, x, y):
        col = 0
        for op, string in self.words:
            dy = 0
            if op == "insert":
                dy = -CHAR_HEIGHT

            text_surface = FONT.render(string, True, LineDrawer.COLORS[op])
            text_rect = text_surface.get_rect(topleft=(x + CHAR_WIDTH * col, y + dy))
            SCREEN.blit(text_surface, text_rect)

            if op != "insert":
                col += len(string)


class Puzzle:
    def __init__(self, game, lines, targets, x=20, y=20, credit=6, speed=10):
        self.game = game
        self.buffer = Buffer(lines)
        self.targets = targets
        self.x, self.y = x, y
        self.credit = credit
        self.speed = speed

    @property
    def lines(self):
        return self.buffer.lines

    @property
    def height(self):
        return 2 * CHAR_HEIGHT * max(self.buffer.rows, len(self.targets))

    @property
    def width(self):
        return CHAR_WIDTH * max(self.buffer.cols, max([len(target) for target in self.targets]))

    def get_rect(self):
        return self.x, self.y, self.width, self.height

    def get_coord(self, row, col):
        return (
            self.x + CHAR_WIDTH * col,
            self.y + CHAR_HEIGHT * (2 * row + 1)
        )

    def get_char(self, row, col):
        line = self.buffer.lines[row]
        if col >= len(line):
            return ""

        return line[col]

    def draw(self):
        # Draw background
        pygame.draw.rect(SCREEN, WORD_BACKGROUND_COLOR, self.get_rect())

        # Draw text
        for n, (line, target) in enumerate(zip(self.lines, self.targets)):
            line = LineDrawer(line, target)
            line.draw(self.x, self.y + (2 * n + 1) * CHAR_HEIGHT)

        buff_no, row, col, _ = NVIM.funcs.getpos(".")
        if NVIM.current.buffer == self.buffer.buffer:
            row -= 1
            col -= 1
            char = self.get_char(row, col)
            x, y = self.get_coord(row, col)
            self.game.mode.draw([(char, x, y)])

        self.y += self.speed / FPS

    def is_solved(self):
        return all([line == target for line, target in zip(self.lines, self.targets)])

    def hit_bottom(self):
        return self.y + self.height + BOTTOM > HEIGHT - CHAR_HEIGHT

    def test(self):
        if self.is_solved() and isinstance(self.game.mode, NormalMode):
            self.game.credit += self.credit
            self.delete()
        elif self.hit_bottom():
            self.game.debit += self.credit * 2
            self.delete()

    def delete(self):
        self.game.puzzles.remove(self)
