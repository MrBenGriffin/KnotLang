# encoding: utf-8
from enum import Enum
from .tool import CutDecorator


@CutDecorator({'O': 'O', 'I': 'I', 'X': 'X', 'H': 'B'})
class Cut(Enum):
    O = 1
    I = 2
    X = 3
    H = 4
    B = 5

    def __str__(self):
        text = {1: "O", 2: "I", 3: "X", 4: "H", 5: "B"}
        return text[self._value_]

    def hex(self):
        bins = {1: 0, 2: 1, 3: 2, 4: 2, 5: 2}
        return bins[self._value_]

