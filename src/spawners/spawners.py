import sys
import inspect

from random import choice
from src.core.puzzles import Puzzle


def get_spawners():
    self = sys.modules[__name__]
    return [obj for name, obj in inspect.getmembers(self, inspect.isclass) if
            obj.__module__ == __name__ and name not in {"RandomSpawner", "Spawner"}]


class RandomSpawner:
    def __init__(self, game, spawners=None):
        self.game = game
        self.spawners = spawners if spawners else get_spawners()
        print(self.spawners)

    def spawn(self):
        if len(self.game.puzzles) < 1:
            cls = choice(self.spawners)
            return cls(self.game)


def get_random_letter():
    return choice("abcdefghijklmnopqrstuvwxyz")


class Spawner:
    def __init__(self, game, texts, targets, par, speed=50):
        puzzle = Puzzle(game, texts, targets, par=par, speed=speed)
        game.puzzles.append(puzzle)


class StartReplaceSpawner(Spawner):
    def __init__(self, game):
        texts = ["The dear fegan to park feer."]
        targets = ["The bear began to bark beer."]
        super().__init__(game, texts=texts, targets=targets, par=8)


class FindReplaceSpawner(Spawner):
    def __init__(self, game):
        texts = ["The feir of mixing out."]
        targets = ["The fear of maxing out."]
        super().__init__(game, texts=texts, targets=targets, par=6)


class StartSpawner(Spawner):
    def __init__(self, game):
        texts = [
            "This is the first item.",
            "This is the second item.",
            "This is the third item."
        ]
        prefix = choice(["-", "+", "[ ]", "[x]"]) + " "
        targets = [prefix + text for text in texts]
        super().__init__(game, texts=texts, targets=targets, par=8)


class EndSpawner(Spawner):
    def __init__(self, game):
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

        super().__init__(game, texts=texts, targets=targets, par=7)


class FindDeleteCharSpawner(Spawner):
    TEXTS = [
        "The quick brown fox jumped.",
        "This is a (sample) word.",
        "Delete all the random characters!"
    ]

    def __init__(self, game):
        target = choice(self.TEXTS)
        inds = list(range(len(target)))
        text = target
        letter = "x"
        count = choice([1, 2, 3])
        for _ in range(count):
            ind = choice(inds)
            inds.remove(ind)
            text = text[:ind] + letter + text[ind:]

        super().__init__(game, [text], [target], par=3 + 2 * count)


class FindDeleteToSpawner(Spawner):
    def __init__(self, game):
        text = "This sentence is short, and this part is not needed."
        target = "This sentence is short."
        super().__init__(game, [text], [target], par=5)


class StartWordInsertSpawner(Spawner):
    def __init__(self, game):
        text = "The sults verted to the original."
        target = "The results reverted to the original."
        super().__init__(game, [text], [target], par=7)


class EndWordInsertSpawner(Spawner):
    def __init__(self, game):
        text = "The test are indicat."
        target = "The testing are indicating."
        super().__init__(game, [text], [target], par=10)


class StartWordDeleteSpawner(Spawner):
    def __init__(self, game):
        text = "I reinstalled my everlong photosynthesis."
        target = "I installed my long synthesis."
        super().__init__(game, [text], [target], par=10)


class EndWordDeleteSpawner(Spawner):
    def __init__(self, game):
        text = "Starting going for the lasting time."
        target = "Start go for the last time."
        super().__init__(game, [text], [target], par=8)


class DeleteWordSpawner(Spawner):
    def __init__(self, game):
        target = "Delete all the repeated words in this sentence."
        text = "Delete delete all the the repeated words words in this this sentence."
        super().__init__(game, [text], [target], par=12)


class SubsSpawner(Spawner):
    def __init__(self, game):
        text = 'var foo = "method("+arg1+","+arg2+");'
        target = 'var foo = "method(" + arg1 + "," + arg2 + ");'
        super().__init__(game, [text], [target], par=8)


class ChangeWordSpawner(Spawner):
    def __init__(self, game):
        target = "The more wine you have, the better your wine tastes."
        text = "The more food you have, the better your food tastes."
        super().__init__(game, [text], [target], par=10)
