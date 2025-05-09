from random import choice
from buffers import Buffer, Line


class RandomSpawner:
    def __init__(self, editor, spawners=None):
        self.editor = editor
        self.spawners = spawners if spawners else []

    def spawn(self):
        return choice(self.spawners)(self.editor)


def letter():
    return choice("abcdefghijklmnopqrstuvwxyz")


class Spawner:
    def __init__(self, editor, name, texts, targets, score):
        lines = [Line(text, target) for text, target in zip(texts, targets)]
        buffer = Buffer(editor, lines, name=name, score=score)
        editor.buffers[buffer.name] = buffer


class EndSpawner(Spawner):
    TEXTS = [
        "This sentence has an error at the end."
    ]

    def __init__(self, editor):
        target = self.TEXTS[0]
        text = target + letter()

        super().__init__(editor, name="a", texts=["Look down", text], targets=["Look down", target], score=3)


class FindSpawner(Spawner):
    TEXTS = [
        "The quick brown fox jumped.",
        "This is a (sample) text.",
        "Don't choose this line, you silly person."
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

        super().__init__(editor, name, [text], [target], count * 3)

    def get_name(self):
        return letter() + ".txt"

class DeleteFindSpawner(Spawner):
    def __init__(self, editor):
        name = None
        text = "You need to delete [this)this unnecessary word."
        target = "You need to delete this unnecessary word."
        super().__init__(editor, name, [text], [target], 4)