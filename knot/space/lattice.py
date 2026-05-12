from abc import ABC, abstractmethod

from .cell import Cell
from .wall import Wall


# https://www.redblobgames.com/grids/hexagons/#coordinates
# https://en.wikipedia.org/wiki/Wallpaper_group#The_seventeen_groups
class Lattice(ABC):

    @abstractmethod
    def set_range(self):
        pass

    @abstractmethod
    def set_cells(self) -> dict:
        pass

    def __init__(self, crs, size: tuple, tiling: set = None):
        tiling = set() if tiling is None else tiling
        self.border = None
        self.offset = None
        self._survey = None
        self.crs = crs
        self.dim = crs.dim()
        self.axes = crs.axis()
        self.size = self.dim.adopt(self.dim.adjust(size))
        self.wrap = self.axes.axes(tiling)
        self.range = self.set_range()
        self.cells = self.set_cells()

    def survey(self):
        from actor import Surveyor
        if self._survey is None:
            surveyor = Surveyor(self)
            self._survey = surveyor.survey()
        return self._survey

    def wall(self, index, com) -> [None, Wall]:
        idx = index if isinstance(index, tuple) else index.tuple()
        return None if idx not in self.cells else self.cells[idx].wall(com)

    def cell(self, index) -> [None, Cell]:
        idx = index if isinstance(index, tuple) else index.tuple()
        return None if idx not in self.cells else self.cells[idx]

    def min(self, ax):
        return min([c[ax] for c in self.cells])

    def max(self, ax):
        return max([c[ax] for c in self.cells])

    def set_border(self, border: [None, int]):
        if border and border > 0:
            blo = self.dim.adopt(tuple(self.size[ax][0] + border for ax in self.axes))
            bhi = self.dim.adopt(tuple(self.size[ax][1] - border for ax in self.axes))
            cell = self.dim.adopt(tuple((0,)))
            for axis in self.axes:
                other = axis.others[0]
                for rv in range(blo[other], bhi[other]):
                    cell.set(other, rv)
                    cell.set(axis, blo[axis])
                    self.cells[cell.tuple()].wall(axis.b).block()
                    cell.set(axis, bhi[axis])
                    self.cells[cell.tuple()].wall(axis.b).block()
            self.border = border
            return border
        return None

    @abstractmethod
    def code(self) -> str:
        pass
