from constants import *
from commands import Command
from movements import *
from finds import *

if __name__ == "__main__":
    EDITOR.buffer = EDITOR.get_buffer(["This is (the) sample text(s).", "Second line."])
    EDITOR.run()