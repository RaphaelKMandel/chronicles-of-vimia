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
    def __init__(self, game, texts, targets, credit, speed=50):
        puzzle = Puzzle(game, texts, targets, credit=credit, speed=speed)
        game.puzzles.append(puzzle)


class ReplaceSpawner(Spawner):
    def __init__(self, game):
        texts = ["The beer wanted to drink bear."]
        targets = ["The bear wanted to drink beer."]
        super().__init__(game, texts=texts, targets=targets, credit=10)


class StartSpawner(Spawner):
    def __init__(self, game):
        texts = [
            "This is the first item.",
            "This is the second item.",
            "This is the third item."
        ]
        prefix = choice(["-", "+", "[ ]", "[x]"]) + " "
        targets = [prefix + text for text in texts]
        super().__init__(game, texts=texts, targets=targets, credit=12)


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

        super().__init__(game, texts=texts, targets=targets, credit=12)


class FindDeleteCharSpawner(Spawner):
    TEXTS = [
        "The quick brown fox jumped.",
        "This is a (sample) text.",
        "Delete all the random characters!"
    ]

    def __init__(self, game):
        target = choice(self.TEXTS)
        inds = list(range(len(target)))
        text = target
        l = get_random_letter()
        max_count = max(3, 2 + int(game.credit // 30))
        for count in range(1, max_count + 1):
            ind = choice(inds)
            inds.remove(ind)
            text = text[:ind] + l + text[ind:]

        super().__init__(game, [text], [target], credit=max_count * 4)


class FindDeleteToSpawner(Spawner):
    def __init__(self, game):
        text = "This sentence is short, and this part is not needed."
        target = "This sentence is short."
        super().__init__(game, [text], [target], credit=10)


class StartWordInsertSpawner(Spawner):
    def __init__(self, game):
        text = "The test sults still needed finishing."
        target = "The test results still needed refinishing."
        super().__init__(game, [text], [target], credit=16)


class EndWordInsertSpawner(Spawner):
    def __init__(self, game):
        text = "The results of the test are indicat."
        target = "The results of the testing are indicating."
        super().__init__(game, [text], [target], credit=16)


class StartWordDeleteSpawner(Spawner):
    def __init__(self, game):
        text = "I reinstalled my everlasting photosynthesis."
        target = "I installed my lasting synthesis."
        super().__init__(game, [text], [target], credit=8)


class EndWordDeleteSpawner(Spawner):
    def __init__(self, game):
        text = "Starting going for lasting night."
        target = "Start going for last night."
        super().__init__(game, [text], [target], credit=8)


class DeleteWordSpawner(Spawner):
    def __init__(self, game):
        target = "Feel free to delete all the repeated words in this sentence."
        text = "Feel free free to delete all all the repeated words words in this sentence."
        super().__init__(game, [text], [target], credit=16)


class SubsSpawner(Spawner):
    def __init__(self, game):
        text = 'var foo = "method("+arg1+","+arg2+");'
        target = 'var foo = "method(" + arg1 + "," + arg2 + ");'
        super().__init__(game, [text], [target], credit=12)


class ChangeWordSpawner(Spawner):
    def __init__(self, game):
        target = "The more wine you have, the better your wine tastes."
        text = "The more food you have, the better your food tastes."
        super().__init__(game, [text], [target], credit=8)
