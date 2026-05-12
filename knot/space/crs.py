from typing import Type
from copy import deepcopy
from abc import ABC, abstractmethod
from enum import Enum
from .lattice import Lattice


class Symmetry(Enum):
    N = 1
    H = 2
    V = 3
    R2 = 4
    R3 = 5
    R6 = 6

    def __str__(self):
        text = {Symmetry.N: "normal/none", Symmetry.H: "mirror on horizontal",
                Symmetry.V: "mirror on vertical",
                Symmetry.R2: "flipped symmetry",
                Symmetry.R3: "3-rotated symmetry",
                Symmetry.R6: "6-rotated symmetry"}
        return text[self]

    @staticmethod
    def choices() -> tuple:
        return 'N', 'H', 'V', 'R2', 'R3', 'R6'


class Axis(Enum):

    @abstractmethod
    def __str__(self):
        pass

    @classmethod
    @abstractmethod
    def axes(cls, tiling: set) -> dict:
        pass

    @classmethod
    @abstractmethod
    def at(cls, key: int):
        pass


class Wallpaper(Enum):
    """
    https://en.wikipedia.org/wiki/Wallpaper_group
    https://en.wikipedia.org/wiki/List_of_planar_symmetry_groups#Wallpaper_groups
    A wallpaper group (or plane symmetry group or plane crystallographic group)
    is a mathematical classification of a two-dimensional repetitive pattern,
    based on the symmetries in the pattern.
    Such patterns occur frequently in architecture and decorative art,
    especially in textiles and tiles as well as wallpaper.

    There are precisely seventeen groups
    p1  = 'master' (only translations; there are no rotations, reflections, or glide reflections) - oblique
    p2  = 'r2' (four rotation centres of order two (180°), but no reflections or glide reflections) - oblique
    pm  = 'vanity/sunset' (no rotations but parallel reflection axes) -  rectangular
    pg  = (only glide reflections with parallel axes) - rectangular
    cm  = (symmetrically staggered rows) - rhombic
    pmm = (mirrored in both vertical and horizontal, not rotated!) - rectangular
    pmg = (mirrored and then glide reflected) - rectangular
    pgg = (reflections in two perpendicular directions, and a rotation of order two (180°) not centred on reflection axis) - rhombic
    cmm = (eg bricks in a wall 'running bond' - rhombic
    p4  = 'r4' (The group p4 has two rotation centres of order four (90°), and one rotation centre of order two (180°) - square
    p4m = (p4 with an internal mirror)
    p4g = (p4 with a glide reflection)
    p3  = 'r3' different rotation centres of order three (120°), but no reflections or glide reflections - hexagonal
    p3m1 = (cf. wikipedia)- hexagonal
    p31m = (cf. wikipedia)- hexagonal
    p6   = 'r6' (cf. wikipedia)- hexagonal
    p6m  = p6 with mirror - hexagonal
    """
    @staticmethod
    def select(val: Symmetry):
        pass

    @classmethod
    def identity(cls):
        return Wallpaper.select(Symmetry.N)

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Coords(ABC):
    def __init__(self, ax: Type[Axis], *args):
        self.axis = ax
        self.dim = dict((ax.at(i), a) for i, a in enumerate(args))

    def delta(self, ax: Axis, value: int):
        self.dim[ax] += value

    def set(self, ax: Axis, value):
        self.dim[ax] = value

    def tuple(self) -> tuple:
        return tuple(self.dim[a] for a in self.axis)

    def bad(self) -> bool:
        for a in self.axis:
            if self.dim[a] is None:
                return True
        return False

    @abstractmethod
    def go(self, com):
        pass

    def __getitem__(self, key):
        if isinstance(key, Axis):
            return self.dim[key]
        return self.tuple().__getitem__(key)

    def __str__(self):
        val = ','.join(str(self.dim[a]) for a in self.axis)
        return "(" + val + ")"

    def __repr__(self):
        val = ','.join(str(self.dim[a]) for a in self.axis)
        return "Dim(" + val + ")"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all(
                other.dim and self.dim[a] == other.dim[a]
                for a in self.axis
            )
        if isinstance(other, tuple):
            return all(
                other[a.idx] and self.dim[a] == other[a.idx]
                for a in self.axis
            )
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return any(
                other.dim and self.dim[a] != other.dim[a]
                for a in self.axis
            )
        if isinstance(other, tuple):
            return any(
                other[a.idx] and self.dim[a] != other[a.idx]
                for a in self.axis
            )
        return NotImplemented

    @classmethod
    @abstractmethod
    def adopt(cls, values: tuple):
        pass

    @classmethod
    @abstractmethod
    def adjust(cls, values: tuple) -> tuple:
        pass

    @classmethod
    @abstractmethod
    def axis(cls, key: int):
        pass

    @classmethod
    @abstractmethod
    def __len__(cls):
        pass

    @classmethod
    @abstractmethod
    def com(cls) -> Type[Enum]:
        pass


class Tweak(ABC):
    @abstractmethod
    def __init__(self, paper: Wallpaper, lattice: Lattice, worker_no: int = 0):
        self.paper = paper
        self.worker_no = worker_no
        self.offset = lattice.offset
        self.coords = None

    @abstractmethod
    def face(self, com: Enum):
        pass

    @abstractmethod
    def dim(self, basis: tuple) -> Coords:
        pass

    @abstractmethod
    def entry(self, border: [int, None]):
        pass

    def __repr__(self):
        return str(self.paper) + " w" + str(self.worker_no) + "; under " + str(self.coords)

    def __str__(self):
        return str(self.paper) + " w" + str(self.worker_no)


class CRS(ABC):
    """
    Coordinate Reference System is an abstract base class.
    """

    @abstractmethod
    def tweak(self, paper: Wallpaper, index: tuple, worker_no: int = 0) -> Tweak:
        pass

    @abstractmethod
    def dim(self) -> Type[Coords]:
        pass

    @abstractmethod
    def axis(self) -> Type[Axis]:
        pass

    @abstractmethod
    def com(self) -> Type[Enum]:
        pass

    @abstractmethod
    def paper(self) -> Type[Wallpaper]:
        pass

    @abstractmethod
    def lattice(self, size: tuple, wrap: tuple) -> Lattice:
        pass


class WallpaperDecorator:
    def __init__(self, wp_map, sym_map):
        self.wp_map = wp_map
        self.sym_map = sym_map

    def __call__(self, enum):
        for thing, workers in self.wp_map.items():
            enum[thing].workers = workers
        for thing, symmetry in self.sym_map.items():
            enum[thing].symmetry = symmetry
        return enum


class AxesDecorator:
    point_map = {}

    def __init__(self, point_map, parallel_map, not_map):
        AxesDecorator.point_map = point_map
        self.parallel_map = parallel_map
        self.not_map = not_map

    def __call__(self, enum):
        for idx, axis in enumerate(AxesDecorator.point_map):
            enum[axis].a = None
            enum[axis].b = None
            enum[axis].idx = idx
        for axis, symmetry in self.parallel_map.items():
            if symmetry:
                enum[axis].para = symmetry[0]
                enum[axis].perp = symmetry[1]
            else:
                enum[axis].para = None
                enum[axis].perp = None
        for axis, others in self.not_map.items():
            enum[axis].others = tuple(enum[i] for i in others)
        return enum


class ComDecorator:
    def __init__(self, start, axis, reverse_map, rotate_map, axis_map):
        self.reverse_map = reverse_map
        self.rotate_map = rotate_map
        self.axis_map = axis_map
        self.axis = axis
        self.start = start

    def __call__(self, enum):
        enum.start = enum[self.start]
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        for fwd, rot in self.rotate_map.items():
            enum[fwd].cw = enum[rot]
            enum[rot].ccw = enum[fwd]
        for com, axis in self.axis_map.items():
            if axis:
                enum[com].axis = self.axis[axis[0]]
                if axis[1] == 0:
                    self.axis[axis[0]].a = enum[com]
                else:
                    self.axis[axis[0]].b = enum[com]
        return enum
