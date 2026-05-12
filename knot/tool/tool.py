from enum import Enum
from abc import ABC, abstractmethod


class Tool(ABC):

    @abstractmethod
    def make(self, com: Enum, cut: Enum = None) -> dict:
        pass


class CutDecorator:
    def __init__(self, reverse_map):
        self.reverse_map = reverse_map

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        return enum
