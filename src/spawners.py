import sys
import inspect

from random import choice
from buffers import Buffer, Line


def get_spawners():
    self = sys.modules[__name__]
    return [obj for name, obj in inspect.getmembers(self, inspect.isclass) if obj.__module__ == __name__]


class RandomSpawner:
    def __init__(self, editor, spawners=None):
        self.editor = editor
        self.spawners = spawners if spawners else get_spawners()
        print(self.spawners)

    def spawn(self):
        return choice(self.spawners)(self.editor)


def letter():
    return choice("abcdefghijklmnopqrstuvwxyz")


class Spawner:
    def __init__(self, editor, name, texts, targets, score):
        lines = [Line(text, target) for text, target in zip(texts, targets)]
        buffer = Buffer(editor, lines, name=name, score=score)
        editor.buffers[buffer.name] = buffer


class StartSpawner(Spawner):
    def __init__(self, editor):
        name = None
        texts = [
            "This is the first item.",
            "This is the second item.",
            "This is the third item."
        ]
        prefix = choice(["-", "+", "[ ]", "[x]"]) + " "
        targets = [prefix + text for text in texts]
        super().__init__(editor, name=name, texts=texts, targets=targets, score=12)


class EndSpawner(Spawner):
    def __init__(self, editor):
        name = None
        targets = [
            "(1) Open the peanut butter.",
            "(2) Put a knife in the peanut butter.",
            "(3) Spread the peanut butter on bread."
        ]
        texts = [
            "(1) Open the peanut butter",
            "(2) Put a knife in the peanut butter",
            "(3) Spread the peanut butter on bread"
        ]

        super().__init__(editor, name=name, texts=texts, targets=targets, score=12)


class FindDeleteCharSpawner(Spawner):
    TEXTS = [
        "The quick brown fox jumped.",
        "This is a (sample) text.",
        "Delete all the random characters!"
    ]

    def __init__(self, editor):
        name = self.get_name()
        target = choice(self.TEXTS)
        inds = list(range(len(target)))
        text = target
        l = letter()
        max_count = max(3, 2 + int(editor.credit // 30))
        for count in range(1, max_count):
            ind = choice(inds)
            inds.remove(ind)
            text = text[:ind] + l + text[ind:]

        super().__init__(editor, name, [text], [target], count * 4)

    def get_name(self):
        return letter() + ".txt"


class FindDeleteToSpawner(Spawner):
    def __init__(self, editor):
        name = None
        text = "This sentence is short, and this part is not needed."
        target = "This sentence is short."
        super().__init__(editor, name, [text], [target], 10)


class StartWordInsertSpawner(Spawner):
    def __init__(self, editor):
        name = None
        text = "The test sults still needed finishing to avoid percussions before submission."
        target = "The test results still needed refinishing to avoid repercussions before resubmission."
        super().__init__(editor, name, [text], [target], 16)


class EndWordInsertSpawner(Spawner):
    def __init__(self, editor):
        name = None
        text = "The results of the test are indicat that the test approach was valid."
        target = "The results of the testing are indicating that the testing approach was valid."
        super().__init__(editor, name, [text], [target], 16)


class StartWordDeleteSpawner(Spawner):
    def __init__(self, editor):
        name = None
        text = "I reinstalled my everlasting photosynthesis."
        target = "I installed my lasting synthesis."
        super().__init__(editor, name, [text], [target], 8)


class EndWordDeleteSpawner(Spawner):
    def __init__(self, editor):
        name = None
        text = "Starting going for lasting night."
        target = "Start going for last night."
        super().__init__(editor, name, [text], [target], 8)


class SubsSpawner(Spawner):
    def __init__(self, editor):
        name = None
        text = 'var foo = "method("+arg1+","+arg2+");'
        target = 'var foo = "method(" + arg1 + "," + arg2 + ");'
        super().__init__(editor, name, [text], [target], 12)
