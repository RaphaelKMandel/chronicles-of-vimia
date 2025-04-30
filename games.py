from constants import *
from commands import Command
from horizontal_movements import *
from vertical_movements import *
from finds import *

if __name__ == "__main__":
    EDITOR.buffer = EDITOR.get_buffer(["This is (the) sample text(s).", "    Second line."])
    EDITOR.run()