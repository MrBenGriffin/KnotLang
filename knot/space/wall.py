# encoding: utf-8
from .cell import Cell


class Wall:

    def __init__(self):
        self.blocked = False
        self.doors = {}
        self.cells = {}

    def cell(self, com) -> [Cell, None]:
        if com not in self.cells:
            return None
        return self.cells[com]

    def make_door(self, com, tool, cut=None, force=False) -> Cell | None:
        # Cut a door with the tool towards comp (from comp.opposite)
        if not self.cells[com] or not self.cells[com.opposite]:
            return None
        if not force and (self.doors or self.blocked):
            return None
        other = self.cells[com]
        start = self.cells[com.opposite]
        self.doors = tool.make(com, cut)
        other.open(tool, com.opposite)
        start.open(tool, com)
        return other

    def make_solid(self, com=None):
        other = self.cells[com] if com else None
        if other and other.opened and other.opened_from == com.opposite:
            other.back_fill()
        self.doors = {}

    def door(self, com):
        """
        Return the door cut-style (or None), according to direction.
        (Some cut-style may appear different depending on what side of the wall
        you are looking through).
        :param com:
        :return:
        """
        if com not in self.doors:
            return None
        return self.doors[com]

    def is_wall(self) -> bool:
        return not self.doors

    def block(self):
        self.blocked = True

    def set_cell(self, cell, com):
        self.cells[com] = cell
        if com.opposite not in self.cells:
            self.cells[com.opposite] = None

    def is_edge(self):  # If on the edge, then one of my wall cells will be None.
        return len(self.cells) != 2

    def can_be_dug(self, com_from) -> bool:
        return not self.cells[com_from].mined() if self.can_be_door(com_from) else False

    def can_be_door(self, com_from) -> bool:
        return not self.doors and com_from in self.cells and self.cells[com_from] and not self.blocked

    def code(self, com):
        return "O" if com not in self.doors else str(self.doors[com])
