from enum import Enum
from typing import Type
from ..crs import CRS, Wallpaper, WallpaperDecorator, Symmetry, Lattice as CRSLattice, Coords
from .lattice import Lattice as HLattice, Lattice
from .tweak import Tweak as HTweak
from .dim import Dim, Com, Axis


class Tweak(HTweak):

    def dim(self, index: tuple) -> Dim:
        # Mirrors in odd-r offset space (col = q + r//2, row = r), then back to cube.
        # Given a worker number and a master cell, work out which cell the worker should be.
        if self.worker_no == 0:
            return index
        basis = Dim.adopt(index)
        adj = Dim.adopt(tuple([a-b for a, b in zip(basis.tuple(), self.offset)]))
        wx = {
            self.paper.sunset: Dim.sunset,
            self.paper.vanity: Dim.vanity,
            self.paper.rotate2: Dim.r2,
            # self.paper.rotate4: Dim.r4
        }
        func = wx[self.paper]
        res = func(adj, self.worker_no)
        adj = Dim.adopt(tuple([a + b for a, b in zip(res.tuple(), self.offset)]))
        return adj



@WallpaperDecorator(
    {'master': 1, 'sunset': 2, 'vanity': 2, 'rotate2': 2},
    {'master': None, 'sunset': Symmetry.H, 'vanity': Symmetry.V, 'rotate2': Symmetry.R2},
)
class Paper(Wallpaper):
    master = 1
    sunset = 2
    vanity = 3
    rotate2 = 4


    @staticmethod
    def select(val: str):
        sel = {'N': Paper.master, 'H': Paper.sunset, 'V': Paper.vanity,
               'R2': Paper.rotate2, 'R3': None, 'R4': None, 'R6': None}
        return sel[val]

    @classmethod
    def identity(cls):
        return Paper.master

    def __str__(self):
        text = {Paper.master: "Master", Paper.sunset: "Sunset",
                Paper.vanity: "Vanity", Paper.mirror: "Mirror"}
        return text[self]

    def __repr__(self):
        return self.__str__()


class Lattice(HLattice):
    def set_cells(self) -> dict:
        _, W = self.size[Axis.W___E]    # W = number of offset columns
        r0, r1 = self.size[Axis.NE_SW]  # row range [0, H)
        cell_coords = set()
        for col in range(0, W):
            parity = col & 1
            for row in range(r0, r1):     # col is the offset column, always [0, W)
                q = col
                r = row - (col - parity) // 2
                if row + 1 == r1 and parity == 1:
                    continue
                cell_coords.add(Dim.axial_to_cube(q, r))
        return super().do_walls(None, cell_coords)


class OddMap(CRS):

    def paper(self) -> Type[Wallpaper]:
        return Paper

    def tweak(self, paper: Wallpaper, index: tuple, worker_no: int = 0) -> Tweak:
        return Tweak(paper, index, worker_no)

    def lattice(self, size: tuple, wrap: set = None) -> CRSLattice:
        W, H = size[0], size[1]
        q_lo = -((H - 1) // 2)
        return Lattice(self, ((q_lo, W), (0, H)), wrap)

    def dim(self) -> Type[Coords]:
        return Dim

    def axis(self) -> Type[Enum]:
        return Axis

    def com(self) -> Type[Enum]:
        return Com
