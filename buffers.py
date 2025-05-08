from constants import *
from diffs import get_diff


class Line:
    COLORS = {
        "insert": GREEN,
        "equal": WHITE,
        "delete": RED
    }

    def __len__(self):
        return len(self.text)

    def __getitem__(self, item):
        return self.text[item]

    def __init__(self, text, target):
        self.augmented = ""
        self.map = []
        self.words = []
        self.target = target
        self.text = text

    def is_solved(self):
        return self.text == self.target

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.update()

    def update(self):
        self.words = get_diff(self.text, self.target)
        self.augmented = "".join([string for _, string in self.words])
        self.get_map()

    def get_map(self):
        self.map = [None] * (len(self.text) + 2)
        n1 = n2 = 0
        for word in self.words:
            if word[0] in {"equal", "delete"}:
                for _ in word[1]:
                    self.map[n1] = n2
                    n1 += 1
                    n2 += 1

            else:
                n2 += len(word[1])

        self.map[n1] = n2

    def get_coord(self, row, col):
        return CHAR_WIDTH * col, CHAR_HEIGHT * row

    def get_x_coord(self, col):
        return CHAR_WIDTH * self.map[col]

    def draw(self, x, y):
        col = 0
        for op, string in self.words:
            text_surface = FONT.render(string, True, Line.COLORS[op])
            text_rect = text_surface.get_rect(topleft=(x + CHAR_WIDTH * col, y))
            SCREEN.blit(text_surface, text_rect)
            col += len(string)


class Buffer:
    def __init__(self, editor, lines: list[Line], x=20, y=20, name=None, score=5):
        self.editor = editor
        self.name = name
        self.lines = lines
        self.row, self.col = 0, 0
        self.x, self.y = x, y
        self.undo_list = []
        self.redo_list = []
        self.score = score

    def get_rect(self):
        max_width = max([len(line.augmented) for line in self.lines])
        return self.x, self.y, max_width * CHAR_WIDTH, len(self.lines) * CHAR_HEIGHT

    def get_coord(self, row, col):
        return (
            self.y + row * CHAR_HEIGHT,
            self.x + self.lines[row].map[col] * CHAR_WIDTH
        )

    @property
    def col(self):
        max_col = self.editor.state.max_col()
        return min(self._col, max_col)

    @col.setter
    def col(self, value):
        self._col = value

    @property
    def line(self):
        return self.lines[self.row].text

    @line.setter
    def line(self, value):
        self.lines[self.row].text = value

    def get_topleft(self, row):
        return self.x, self.y + row * CHAR_HEIGHT

    def next_row(self):
        if self.row == len(self.lines) - 1:
            return False

        self.row += 1
        return True

    def previous_row(self):
        if self.row == 0:
            return False

        self.row -= 1
        return True

    def draw(self):
        # Draw background
        pygame.draw.rect(SCREEN, WORD_BACKGROUND_COLOR, self.get_rect())

        # Draw text
        for n, line in enumerate(self.lines):
            line.draw(self.x, self.y + CHAR_HEIGHT * n)

        self.y += 0.01 * self.editor.credit

        # footer = FONT.render(self.name, True, WHITE)
        # x, y, l, h = self.get_rect()
        # footer_rect = footer.get_rect(topleft=(x, y + h))
        # self.editor.screen.blit(footer, footer_rect)
        #
        # footer = FONT.render(f"Points: {self.score}", True, WHITE)
        # x, y, l, h = self.get_rect()
        # footer_rect = footer.get_rect(topleft=(x + l - CHAR_WIDTH * 10, y + h))
        # self.editor.screen.blit(footer, footer_rect)

    def is_solved(self):
        return all([line.is_solved() for line in self.lines])

    def hit_bottom(self):
        height = len(self.lines) * CHAR_HEIGHT + self.editor.BOTTOM
        return self.y + height > HEIGHT - CHAR_HEIGHT

    def test(self):
        if self.is_solved():
            self.editor.credit += self.score
            del self.editor.buffers[self.name]
        elif self.hit_bottom():
            self.destroy()

    def destroy(self):
        self.editor.count += self.score * 2
        del self.editor.buffers[self.name]
        self.editor.state = self.editor.normal
