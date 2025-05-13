from src.core.states import NormalMode
from src.core.actions.finds import *
from src.core.actions.horizontal_movements import *
from src.core.actions.mementos import *
from src.core.actions.vertical_movements import *
from src.core.changes.inserts import *
from src.core.changes.instant_changes import *
from src.core.changes.operator_changes import *

KEYMAP = {
    NormalMode: {

        "h": MoveLeft,
        "l": MoveRight,
        "0": MoveZero,
        "^": MoveCarrot,
        "_": MoveCarrot,
        "$": MoveDollar,
        "w": MoveStartWord,
        "e": MoveEndWord,
        "b": MovePrevWord,

        "f": FindForwardMovement,
        "F": FindBackwardMovement,
        "t": FindForwardToMovement,
        "T": FindBackwardToMovement,
        ";": RepeatFindForwardMovement,
        ",": RepeatFindBackwardMovement,

        "j": MoveDown,
        "k": MoveUp,

        "u": Undo,
        "U": Redo,  # My preferred keybind
        "\x12": Redo,  # Default keybind <C-R>

        "i": InsertChange,
        "a": AppendChange,
        "I": InsertAtStartChange,
        "A": AppendAtEndChange,
        "s": SubsChange,

        "x": DeleteChange,
        "X": BackspaceChange,
        "r": ReplaceChange,
        ".": RepeatLastChange,

        "d": DeleteOperator,
        "c": ChangeOperator,
    },
    OperatorMode: {
        "f": FindForwardAction,
        "F": FindBackwardAction,
        "t": FindForwardToAction,
        "T": FindBackwardToAction,

        "w": StartWordAction,
        "e": EndWordAction,
        "b": PrevWordAction,
    }
}


def set_keymaps(include=None, exclude=None):
    include = include if include is not None else KEYMAP
    for mode, values in include.items():
        for key, value in values.items():
            mode.KEYMAP[key] = value

    exclude = exclude if exclude is not None else {}
    for mode, values in exclude.items():
        for key in values:
            del mode.KEYMAP[key]
