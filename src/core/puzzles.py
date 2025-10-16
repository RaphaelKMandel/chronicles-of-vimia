from .constants import *
from .modes import NormalMode
from .buffers import Buffer
from .diffs import get_diff


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
    def __init__(self, game, lines, par, x=20, y=20):
        self.game = game
        self.buffer = Buffer(lines)
        self.par = par
        self.x, self.y = x, y

    @property
    def lines(self):
        return self.buffer.lines

    @property
    def height(self):
        return CHAR_HEIGHT * self.buffer.rows

    @property
    def width(self):
        return CHAR_WIDTH * self.buffer.cols

    def get_rect(self):
        return self.x, self.y, self.width, self.height

    def get_coord(self, row, col):
        return (
            self.get_x_coord(col),
            self.get_y_coord(row)
        )

    def get_x_coord(self, col):
        return self.x + CHAR_WIDTH * col

    def get_y_coord(self, row):
        return self.y + CHAR_HEIGHT * row

    def draw_background(self):
        # Draw background
        pygame.draw.rect(SCREEN, WORD_BACKGROUND_COLOR, self.get_rect())

    def draw_text(self):
        # Draw text
        for n, line in enumerate(self.lines):
            draw_text(line, self.x, self.get_y_coord(n), WHITE)

    def get_char(self, row, col):
        line = self.buffer.lines[row]
        if col >= len(line):
            return ""

        return line[col]

    def draw_cursor(self):
        buff_no, row, col, _ = NVIM.funcs.getpos(".")
        if NVIM.current.buffer != self.buffer.buffer:
            return

        row -= 1
        col -= 1

        mode = NVIM.funcs.mode()

        # Visual mode selection
        if mode == "v":
            start_row, start_col = [p - 1 for p in NVIM.funcs.getpos("v")[1:3]]
            self.draw_visual_selection(start_row, start_col, row, col)
        else:
            char = self.get_char(row, col)
            x, y = self.get_coord(row, col)
            self.game.mode.draw([(char, x, y)])

    def draw_visual_selection(self, start_row, start_col, end_row, end_col):
        """Draw highlighted area between start and end inclusive."""
        if start_row > end_row or (start_row == end_row and start_col > end_col):
            start_row, start_col, end_row, end_col = end_row, end_col, start_row, start_col

        items = []
        for r in range(start_row, end_row + 1):
            line = self.buffer.lines[r]
            c_start = start_col if r == start_row else 0
            c_end = end_col if r == end_row else len(line) - 1
            for c in range(c_start, c_end + 1):
                char = self.get_char(r, c)
                x, y = self.get_coord(r, c)
                items.append((char, x, y))
        self.game.mode.draw(items)

    def draw_extra(self):
        pass

    def draw(self):
        self.draw_background()
        self.draw_text()
        self.draw_cursor()
        self.draw_extra()
        self.update()

    def update(self):
        pass

    def is_solved(self):
        pass

    def is_failed(self):
        pass

    def test(self):
        if self.is_solved() and isinstance(self.game.mode, NormalMode):
            self.game.credit += self.game.multiplier * self.par
            self.delete()
        elif self.is_failed():
            self.delete()

    def delete(self):
        self.game.puzzles.remove(self)


class FallingPuzzle(Puzzle):
    def __init__(self, game, lines, par, x, y, speed=50):
        super().__init__(game, lines, par, x, y)
        self.speed = speed

    def update(self):
        self.y += self.speed / FPS

    def is_failed(self):
        return self.y + self.height + BOTTOM > HEIGHT - CHAR_HEIGHT


class EditPuzzle(FallingPuzzle):
    def __init__(self, game, lines, targets, x=20, y=20, par=6, speed=10):
        super().__init__(game, lines, par, x, y, speed)
        self.targets = targets

    @property
    def height(self):
        return 2 * CHAR_HEIGHT * max(self.buffer.rows, len(self.targets))

    @property
    def width(self):
        return CHAR_WIDTH * max(self.buffer.cols, max([len(target) for target in self.targets]))

    def get_y_coord(self, row):
        return self.y + CHAR_HEIGHT * (2 * row + 1)

    def draw_text(self):
        # Draw text
        for n, (line, target) in enumerate(zip(self.lines, self.targets)):
            line = LineDrawer(line, target)
            line.draw(self.x, self.get_y_coord(n))

    def is_solved(self):
        return all([line == target for line, target in zip(self.lines, self.targets)])


class MovementPuzzle(FallingPuzzle):
    def __init__(self, game, x, y, speed, n_rows, n_cols, rows, cols):
        lines = [" " * n_cols] * n_rows
        self.rows = rows
        self.cols = cols
        par = 0
        rowp = colp = 0
        for row, col in zip(self.rows, self.cols):
            par += abs(row-rowp) + abs(col-colp)
            rowp, colp = row, col


        super().__init__(game, lines, par, x, y, speed)

    def is_solved(self):
        buff_no, row, col, _ = NVIM.funcs.getpos(".")
        if self.rows[-1] == row - 1 and self.cols[-1] == col - 1:
            self.rows.pop()
            self.cols.pop()
        return len(self.rows) == 0

    def draw_extra(self):
        char = self.get_char(self.rows[-1], self.cols[-1])
        x, y = self.get_coord(self.rows[-1], self.cols[-1])
        pygame.draw.rect(SCREEN, ORANGE, (x, y, CHAR_WIDTH, CHAR_HEIGHT))
        draw_text(char, x, y, CURSOR_TEXT_COLOR)
