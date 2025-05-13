from src.core.editors import Editor
from src.spawners.spawners import *
from src.core.keybinds import *


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

    # EDITOR.spawner.spawners = [FindSpawner, EndSpawner, DeleteFindSpawner]

    editor = Editor()
    editor.spawner = RandomSpawner(editor)
    # editor.spawner.spawners = [ChangeWordSpawner]
    set_keymaps()
    editor.run()
