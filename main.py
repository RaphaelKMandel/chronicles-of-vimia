from constants import *
from commands import *
from horizontal_movements import *
from words import *
from vertical_movements import *
from inserts import *
from finds import *
from mementos import *
from instant_actions import *
from spawners import *

if __name__ == "__main__":
    # lines = [
    #     "class Foo:",
    #     "    def foo(self, x):   ",
    #     "       return self.x + 1"
    # ]
    # test_lines = [
    #     "class Foo:",
    #     "    def foo(self):",
    #     "       return self.x + 1"
    # ]
    # EDITOR.add_buffer("main.py", lines, test_lines)
    # EDITOR.buffer = EDITOR.buffers["main.py"]


    EDITOR.spawner.spawners = [FindSpawner, EndSpawner]
    EDITOR.run()
