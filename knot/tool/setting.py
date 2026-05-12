# encoding: utf-8
import random
from knot.tool.cut import Cut

class Setting:
    def __init__(self, straights_balance=0.2, spaces_balance=0.0, rng=random):
        self.straights_balance = straights_balance
        self.spaces_balance = spaces_balance
        self.rng = rng

    def choose(self) -> Cut:
        if self.rng.random() < self.spaces_balance:
            return Cut.O
        if self.rng.random() >= self.straights_balance:
            return Cut.X
        return Cut.I
