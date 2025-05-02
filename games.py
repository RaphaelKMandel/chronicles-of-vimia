from constants import *
from commands import Command
from horizontal_movements import *
from vertical_movements import *
from inserts import *
from finds import *
from mementos import *
from instant_actions import *


if __name__ == "__main__":
    lines = [
        "This is (the) sample text(s).",
        "    Second line.",
        "Third line is some length?"
    ]
    EDITOR.buffer = EDITOR.get_buffer(lines)
    EDITOR.run()
