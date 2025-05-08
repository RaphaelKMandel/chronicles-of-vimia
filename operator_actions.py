from classes import OperatorMode
from actions import CompoundAction
from words import EndWord


class OperatorAction(CompoundAction):
    def __init__(self, parent):
        super().__init__(parent)
        self.state = OperatorMode(self)


class DeleteOperator(OperatorAction):

    def deactivate(self):
        self.actions += []



class EndWordOperator(EndWord):
