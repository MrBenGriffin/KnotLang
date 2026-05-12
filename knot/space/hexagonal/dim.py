from enum import IntEnum
from copy import deepcopy  # used by Dim.edge
from ..crs import Coords, AxesDecorator, ComDecorator, Symmetry, Axis as CRSAxis


# There are three axes to a hexagon, regardless of the lattice shape.
# q = from SW_NE, r = N___S, s  = SE_NW
# W___E  x (W  == -x)
# SE_NW  y (SE == -x)
# NE_SW  z (NE == -z)

@AxesDecorator(
    {'W___E': None, 'SE_NW': None, 'NE_SW': None},
    {'W___E': (Symmetry.V, Symmetry.H), 'SE_NW': None, 'NE_SW': None},
    {'W___E': ['SE_NW', 'NE_SW'], 'NE_SW': ['SE_NW', 'W___E'], 'SE_NW': ['NE_SW', 'W___E']}
)
class Axis(CRSAxis):
    W___E = 0x0100
    SE_NW = 0x0200
    NE_SW = 0x0400

    def __str__(self):
        text = {Axis.NE_SW: "NE.SW", Axis.W___E: "WE", Axis.SE_NW: "SE.NW"}
        return text[self]

    @classmethod
    def at(cls, key: int):
        return (Axis.W___E, Axis.SE_NW, Axis.NE_SW)[key]

    @classmethod
    def axes(cls, tiling: set) -> dict:
        result = {Axis.W___E: False, Axis.SE_NW: False, Axis.NE_SW: False}
        if tiling:
            answers = {"NE.SW": Axis.NE_SW, "WE": Axis.W___E, "SE.NW": Axis.SE_NW}
            for tile in tiling:
                if tile in answers:
                    result[answers[tile]] = True
                else:
                    print("Axis", tile, "is not recognised for hexagonal tiling. Use WE, NE.SW, and SE.NW")
        return result


@ComDecorator(
    'NN', Axis,
    {'NN': 'SS', 'NW': 'SE', 'NE': 'SW'},
    {'NN': 'NE', 'NE': 'SE', 'SE': 'SS', 'SS': 'SW', 'SW': 'NW', 'NW': 'NN'},
    {'NN': ['W___E', 1], 'SS': ['W___E', 0], 'NE': ['NE_SW', 0],  'SW': ['NE_SW', 1], 'SE': ['SE_NW', 0], 'NW': ['SE_NW', 1]}
)
class Com(IntEnum):
    # base 3, from most sig to least sig.  243, 81, 27, 9, 3, 1
    NN = 243
    NE = 81
    SE = 27
    SS = 9
    SW = 3
    NW = 1

    def __str__(self):
        text = {Com.NN: "North", Com.NE: "N.East", Com.SE: "S.East", Com.SS: "South", Com.SW: "S.West", Com.NW: "N.West"}
        return text[self]


class Dim(Coords):
    # https://www.redblobgames.com/grids/hexagons/implementation.html#hex
    def __init__(self, *args):
        super().__init__(Axis, *args)

    def go(self, com):
        offsets = {
            Com.NN: Dim(0, +1, -1),  # √
            Com.NE: Dim(+1, 0, -1),  # √
            Com.SE: Dim(+1, -1, 0),  # √
            Com.SS: Dim(0, -1, +1),  # √
            Com.SW: Dim(-1, 0, +1),  # √
            Com.NW: Dim(-1, +1, 0)   # √
        }
        offset = offsets[com]
        for a in Axis:
            self.dim[a] += offset.dim[a]

    def sunset(self, count):
        # Identity: Axis.W___E, Axis.SE_NW, Axis.NE_SW
        if count % 2 == 1:
            return Dim(self.dim[Axis.W___E], self.dim[Axis.NE_SW], self.dim[Axis.SE_NW])
        else:
            return self

    def vanity(self, count):
        if count % 2 == 1:
            return Dim(- self.dim[Axis.W___E], -self.dim[Axis.NE_SW], -self.dim[Axis.SE_NW])
        else:
            return self

    def r2(self, count):
        if count % 2 == 1:
            return Dim(- self.dim[Axis.W___E], - self.dim[Axis.SE_NW], - self.dim[Axis.NE_SW])
        else:
            return self

    def r6(self, count):
        base = list(self.dim.values())
        for i in range(count):
            # rotate right
            #                 W___E , SE_NW , NE_SW     0
            #        -NE_SW, -W___E, -SE_NW             60
            base = [-base[2], -base[0], -base[1]]
        return Dim(base[0], base[1], base[2])

    def r3(self, count):
        # rotate right
        # W___E , SE_NW , NE_SW     0
        # SE_NW,  NE_SW,  W___E     120
        base = list(self.dim.values())
        for i in range(count):
            base = [base[1], base[2], base[0]]
        return Dim(base[0], base[1], base[2])

    def tr3(self, count, size):
        # rotate right AND translate.
        base = list(self.dim.values())
        for i in range(count):
            base = [base[1] + size, base[2] - size, base[0]]
        return Dim(base[0], base[1], base[2])

    def edge(self, com, edge_boundaries: dict, wraps):
        # Given a cell dim and a com, return the edge dim for the edge at that com.
        # limits are a dict of tuples of min/max against an axis.
        dxy = deepcopy(self)
        if com == com.axis.a:
            dxy.go(com)
        return dxy

    @classmethod
    def axial_to_cube(cls, q, r):
        return q, -q - r, r

    @classmethod
    def odd_to_cube(cls, col, row):
        x = col
        z = row - ((col - (col & 1)) >> 1)
        return x, -x - z, z

    @staticmethod
    def cube_to_axial(q, r, s):
        return q, r

    @staticmethod
    def cube_to_odd(q, r, s):
        parity = q & 1
        col = q
        row = r + (q - parity) // 2
        return col, row

    @classmethod
    def com(cls):
        return Com

    @classmethod
    def axis(cls, key: int):
        return Axis.W___E if key == 0 else Axis.SE_NW if key == 1 else Axis.NE_SW if key == 2 else None

    @classmethod
    def adjust(cls, a: tuple) -> tuple:
        len_a = len(a)
        match len_a:
            case 1:
                d = int(a[0])
                return d, d
            case 2:
                b, c = a
                return b, c
            case _: return None


    @classmethod
    def adopt(cls, a: tuple):
        return None if not a \
            else Dim(a[0], a[0], a[0]) if len(a) == 1 \
            else Dim(a[0], (-a[0][0]-a[1][0], -a[0][1]-a[1][1]), a[1]) if len(a) == 2 and isinstance(a[0], tuple) \
            else Dim(a[0], - a[0] - a[1], a[1]) if len(a) == 2 \
            else Dim(*a) if len(a) == 3 \
            else None

    @classmethod
    def __len__(cls):
        return 3
