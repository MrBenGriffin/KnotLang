from enum import Enum
from typing import Type
from ..crs import CRS, Wallpaper, WallpaperDecorator, Symmetry, Lattice as CRSLattice, Coords
from .lattice import Lattice as HLattice
from .tweak import Tweak as RTweak
from .dim import Dim, Com, Axis


@WallpaperDecorator(
    {'master': 1, 'rotate2': 2},
    {'master': Symmetry.N, 'rotate2': Symmetry.R2},
)
class Paper(Wallpaper):
    master = 1
    rotate2 = 2

    @staticmethod
    def select(val: str):
        sel = {'N': Paper.master, 'H': None,
               'V': None, 'R3': None, 'R2': Paper.rotate2, 'R4': None, 'R6': None}
        return sel[val]

    @classmethod
    def identity(cls):
        return Paper.master

    def __str__(self):
        text = {Paper.master: "Master", Paper.rotate2: "Rotate 2"}
        return text[self]

    def __repr__(self):
        return self.__str__()


class Tweak(RTweak):

    def dim(self, index: tuple) -> Dim:
        if self.worker_no == 0:
            return index
        basis = Dim.adopt(index)
        adj = Dim.adopt(tuple([a-b for a, b in zip(basis.tuple(), self.offset)]))
        res = Dim.r2(adj, self.worker_no)
        adj = Dim.adopt(tuple([a + b for a, b in zip(res.tuple(), self.offset)]))
        return adj


class Lattice(HLattice):
    # Rhombus
    def set_cells(self) -> dict:
        q0, q1 = self.size[Axis.W___E]
        r0, r1 = self.size[Axis.NE_SW]
        cell_coords = set()
        for q in range(q0, q1):
            for r in range(r0, r1):
                cell_coords.add(Dim.axial_to_cube(q, r))
        return super().do_walls(None, cell_coords)


class Rhombus(CRS):

    def paper(self) -> Type[Wallpaper]:
        return Paper

    def tweak(self, paper: Wallpaper, lattice: Lattice, worker_no: int = 0) -> Tweak:
        return Tweak(paper, lattice, worker_no)

    def lattice(self, size: tuple, wrap: set = None) -> CRSLattice:
        return Lattice(self, tuple((0, s) for s in size), wrap)

    def dim(self) -> Type[Coords]:
        return Dim

    def axis(self) -> Type[Enum]:
        return Axis

    def com(self) -> Type[Enum]:
        return Com
