from src.core.constants import *
from src.core.states import State
from src.core.actions.changes import Delete, Backspace, InsertChar


class InsertMode(State):
    KEYMAP = {}
    NAME = "-- INSERT --"

    def __init__(self, editor, parent):
        super().__init__(editor)
        self.parent = parent
        self.actions = []

    def max_col(self):
        return len(self.editor.buffer.line)

    def handle_input(self, event):
        if event.key == pygame.K_ESCAPE:
            print("states:", self.editor.states)
            self.parent.finish()
            return

        if event.key == pygame.K_BACKSPACE:
            action = Backspace(self.editor)
            self.actions.append(action)
            action.execute()

        if event.key == pygame.K_DELETE:
            action = Delete(self.editor)
            self.actions.append(action)
            action.execute()

        if event.unicode.isprintable():
            action = InsertChar(self.editor, event.unicode)
            self.actions.append(action)
            action.execute()

    def draw(self):
        super().draw()

        # Draw cursor as a block
        top, left = self.editor.buffer.get_coord(self.editor.buffer.row, self.editor.buffer.col)
        cursor_rect = pygame.Rect(left, top, CHAR_WIDTH // 4, CHAR_HEIGHT)

        # Draw the cursor
        pygame.draw.rect(SCREEN, CURSOR_COLOR, cursor_rect)
