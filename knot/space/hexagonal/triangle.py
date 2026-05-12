from enum import Enum
from typing import Type
from ..crs import CRS, Coords, Wallpaper, WallpaperDecorator, Symmetry, Lattice as CRSLattice
from .lattice import Lattice as HLattice
from .tweak import Tweak as HTweak
from .dim import Axis, Com, Dim


@WallpaperDecorator(
    {'master': 1, 'sunset': 2, 'rotate3': 3},
    {'master': Symmetry.N, 'sunset': Symmetry.H, 'rotate3': Symmetry.R3},
)
class Paper(Wallpaper):
    master = 1
    sunset = 2
    rotate3 = 3
    rotate6 = 0
    vanity = 0
    rotate2 = 0

    @staticmethod
    def select(val: str):
        sel = {'N': Paper.master, 'H': Paper.sunset,
               'V': None, 'R2': None, 'R3': Paper.rotate3, 'R4': None, 'R6': None}
        return sel[val]

    @classmethod
    def identity(cls):
        return Paper.master

    def __str__(self):
        text = {Paper.master: "Master", Paper.sunset: "Sunset", Paper.rotate3: "Rotate 3"}
        return text[self]

    def __repr__(self):
        return self.__str__()


class Tweak(HTweak):
    # Given a worker number and a master cell, work out which cell the worker should be.
    def dim(self, index: tuple) -> Dim:
        # Mirrors in odd-r offset space (col = q + r//2, row = r), then back to cube.
        # Given a worker number and a master cell, work out which cell the worker should be.
        if self.worker_no == 0:
            return index
        basis = Dim.adopt(index)
        adj = Dim.adopt(tuple([a-b for a, b in zip(basis.tuple(), self.offset)]))
        wx = {
            self.paper.rotate3: Dim.r3,
            self.paper.sunset: Dim.sunset,
            self.paper.rotate6: None,
            self.paper.vanity: None,
            self.paper.rotate2: None
        }
        res = wx[self.paper](adj, self.worker_no)
        adj = Dim.adopt(tuple([a + b for a, b in zip(res.tuple(), self.offset)]))
        return adj


class Lattice(HLattice):

    # The triangle points to the East (ie., the vertical edge is on the left).
    def set_cells(self) -> dict:
        map_range = self.size[0]
        cell_coords = set()
        map_length = map_range[1]
        for q in range(map_range[0], map_length):
            for r in range(0, map_length - q):
                cc_tuple = Dim.axial_to_cube(q, r)
                cell_coords.add(cc_tuple)
        return super().do_walls(None, cell_coords)


class Triangle(CRS):

    def paper(self) -> Type[Wallpaper]:
        return Paper

    def tweak(self, paper: Wallpaper, lattice: Lattice, worker_no: int = 0) -> Tweak:
        return Tweak(paper, lattice, worker_no)

    def lattice(self, size: tuple, wrap: set = None) -> CRSLattice:
        return Lattice(self, tuple(tuple((0, s + 1)) for s in size), wrap)

    def dim(self) -> Type[Coords]:
        return Dim

    def axis(self) -> Type[Enum]:
        return Axis

    def com(self) -> Type[Enum]:
        return Com
