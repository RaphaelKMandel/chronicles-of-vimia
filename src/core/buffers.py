from .constants import *


class Buffer:
    def __init__(self, lines):
        NVIM.command("enew")
        self.buffer = NVIM.current.buffer
        self.no = self.buffer.number
        NVIM.command(f"file /temp/{self.no}")
        NVIM.command("setlocal undolevels=-1")
        self.buffer[:] = lines
        NVIM.input("<esc>")
        NVIM.command("setlocal nomodified")
        NVIM.command("setlocal undolevels=100")

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

    @property
    def cols(self):
        return max([len(line) for line in self.lines])

    @property
    def rows(self):
        return len(self.lines)


