import sys
import inspect
from random import choice

from ..puzzles import EditPuzzle, MovementPuzzle


def get_spawners():
    self = sys.modules[__name__]
    return [obj for name, obj in inspect.getmembers(self, inspect.isclass) if
            obj.__module__ == __name__ and name not in {"RandomSpawner", "Spawner", "EditSpawner"}]


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


class EditSpawner:
    def __init__(self, game, texts, targets, par, speed=50):
        puzzle = EditPuzzle(game, texts, targets, par=par, speed=speed)
        game.puzzles.append(puzzle)


class StartReplaceSpawner(EditSpawner):
    def __init__(self, game):
        texts = ["The dear fegan to park feer."]
        targets = ["The bear began to bark beer."]
        super().__init__(game, texts=texts, targets=targets, par=10)


class EndReplaceSpawner(EditSpawner):
    def __init__(self, game):
        texts = ["The bean used tan to ban the can."]
        targets = ["The bear used tar to bar the car."]
        super().__init__(game, texts=texts, targets=targets, par=13)


class FindReplaceSpawner(EditSpawner):
    def __init__(self, game):
        texts = ["The feir of mixing out."]
        targets = ["The fear of maxing out."]
        super().__init__(game, texts=texts, targets=targets, par=6)


class StartSpawner(EditSpawner):
    def __init__(self, game):
        texts = [
            "This is the first item.",
            "This is the second item.",
            "This is the third item."
        ]
        prefix = choice(["-", "+", "[ ]", "[x]"]) + " "
        targets = [prefix + text for text in texts]
        super().__init__(game, texts=texts, targets=targets, par=8)


class EndSpawner(EditSpawner):
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


class FindDeleteCharSpawner(EditSpawner):
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

        super().__init__(game, [text], [target], par=3 + 2 * (count - 1))


class FindDeleteToSpawner(EditSpawner):
    def __init__(self, game):
        text = "This sentence is short, and this part is not needed."
        target = "This sentence is short."
        super().__init__(game, [text], [target], par=5)


class StartWordInsertSpawner(EditSpawner):
    def __init__(self, game):
        text = "The sults verted to the original."
        target = "The results reverted to the original."
        super().__init__(game, [text], [target], par=7)


class EndWordInsertSpawner(EditSpawner):
    def __init__(self, game):
        text = "The test are indicat."
        target = "The testing are indicating."
        super().__init__(game, [text], [target], par=10)


class StartWordDeleteSpawner(EditSpawner):
    def __init__(self, game):
        text = "I reinstated my everlong photosynthesis."
        target = "I instated my long synthesis."
        super().__init__(game, [text], [target], par=10)


class EndWordDeleteSpawner(EditSpawner):
    def __init__(self, game):
        text = "Starting going for the lasting time."
        target = "Start go for the last time."
        super().__init__(game, [text], [target], par=8)


class DeleteWordSpawner(EditSpawner):
    def __init__(self, game):
        target = "Please delete all the repeated words."
        text = "Please delete delete all the the repeated words words."
        super().__init__(game, [text], [target], par=9)


class SubsSpawner(EditSpawner):
    def __init__(self, game):
        text = 'var foo = "method("+arg1+","+arg2+");'
        target = 'var foo = "method(" + arg1 + "," + arg2 + ");'
        super().__init__(game, [text], [target], par=13)


class ChangeWordSpawner(EditSpawner):
    def __init__(self, game):
        target = "The more wine you have, the better your wine tastes."
        text = "The more food you have, the better your food tastes."
        super().__init__(game, [text], [target], par=10)


class DeleteAroundWordSpawner(EditSpawner):
    def __init__(self, game):
        targets = [
            "The first sign of you",
            "Is impeccable timing",
            "A simple poem"
        ]
        texts = [
            "The first sign sign of you",
            "Is impeccable impeccable timing",
            "A simple simple poem"
        ]
        super().__init__(game, texts, targets, par=8)


class ChangeToEndSpawner(EditSpawner):
    def __init__(self, game):
        texts = ["You know I love you, but you always do that"]
        targets = ["You know I love you."]
        super().__init__(game, texts, targets, par=5)


class DeleteToEndSpawner(EditSpawner):
    def __init__(self, game):
        texts = ["I cant believe you did that, you always do that!"]
        targets = ["I cant believe you did that"]
        super().__init__(game, texts, targets, par=3)


class MovementSpawner:
    def __init__(self, game):
        n_rows = 5
        n_cols = 11
        N = 1
        rows = [choice(range(n_rows)) for _ in range(1)]
        cols = [choice(range(n_cols)) for _ in range(1)]
        puzzle = MovementPuzzle(game, x=20, y=20, speed=50, n_rows=5, n_cols=11, rows=rows, cols=cols)
        game.puzzles.append(puzzle)