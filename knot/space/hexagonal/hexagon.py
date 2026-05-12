from enum import Enum
from typing import Type
from ..crs import CRS, Coords, Wallpaper, WallpaperDecorator, Symmetry, Lattice as CRSLattice
from .lattice import Lattice as HLattice
from .tweak import Tweak as HTweak
from .dim import Axis, Com, Dim

class Tweak(HTweak):

    def dim(self, index: tuple) -> Dim:
        # Mirrors in odd-r offset space (col = q + r//2, row = r), then back to cube.
        # Given a worker number and a master cell, work out which cell the worker should be.
        if self.worker_no == 0:
            return index
        basis = Dim.adopt(index)
        adj = Dim.adopt(tuple([a-b for a, b in zip(basis.tuple(), self.offset)]))
        wx = {
            self.paper.rotate3: Dim.r3,
            self.paper.rotate6: Dim.r6,
            self.paper.sunset: Dim.sunset,
            self.paper.vanity: Dim.vanity,
            self.paper.rotate2: Dim.r2
        }
        res = wx[self.paper](adj, self.worker_no)
        adj = Dim.adopt(tuple([a + b for a, b in zip(res.tuple(), self.offset)]))
        return adj



@WallpaperDecorator(
    # for thing, workers in self.wp_map.items(): enum[thing].workers = workers
    # for thing, symmetry in self.sym_map.items(): enum[thing].symmetry = symmetry
    {'master': 1, 'sunset': 2, 'vanity': 2, 'rotate2': 2, 'rotate3': 3, 'rotate6': 6},
    {'master': Symmetry.N, 'sunset': Symmetry.H, 'vanity': Symmetry.V,
     'rotate2': Symmetry.R2, 'rotate3': Symmetry.R3, 'rotate6': Symmetry.R6},
)
class Paper(Wallpaper):
    master = 1
    sunset = 2
    vanity = 3
    rotate2 = 4
    rotate3 = 5
    rotate6 = 6

    @staticmethod
    def select(val: str):
        sel = {'N': Paper.master, 'H': Paper.sunset, 'V': Paper.vanity,
               'R2': Paper.rotate2, 'R3': Paper.rotate3, 'R4': None, 'R6': Paper.rotate6}
        return sel[val]

    @classmethod
    def identity(cls):
        return Paper.master

    def __str__(self):
        text = {Paper.master: "Master", Paper.sunset: "Sunset",
                Paper.vanity: "Vanity", Paper.rotate2: "Rotate 2", Paper.rotate3: "Rotate 3", Paper.rotate6: "Rotate 6"}
        return text[self]

    def __repr__(self):
        return self.__str__()


class Lattice(HLattice):
    def _text_cell_exits(self):
        return 5

    def set_cells(self) -> dict:
        wall_dims = dict(
            (self.dim.axis(i), self.size[:i] + (adj,) + self.size[i + 1:]) for i, adj in enumerate(self.range))
        q_range = self.size[Axis.W___E]
        r_range = self.size[Axis.NE_SW]
        q0, q1 = q_range
        r0, r1 = r_range
        n = (q1 - q0) // 2
        cell_coords = set()
        for dq in range(q1 - q0):
            q = q0 + dq
            r_lo = r0 + max(0, n - dq)
            r_hi = r0 + min(2 * n + 1, 3 * n - dq + 1)
            for r in range(r_lo, r_hi):
                cell_coords.add(Dim.axial_to_cube(q, r))
        return super().do_walls(wall_dims, cell_coords)

    def set_border(self, border: [None, int]):
        return


class Hexagon(CRS):

    def paper(self) -> Type[Wallpaper]:
        return Paper

    def tweak(self, paper: Wallpaper, index: tuple, worker_no: int = 0) -> Tweak:
        return Tweak(paper, index, worker_no)

    def lattice(self, size: tuple, wrap: set = None) -> CRSLattice:
        n = min(size) // 2
        return Lattice(self, tuple((0, 2 * n + 1) for _ in size), wrap)

    def dim(self) -> Type[Coords]:
        return Dim

    def axis(self) -> Type[Enum]:
        return Axis

    def com(self) -> Type[Enum]:
        return Com
