# encoding: utf-8
from abc import ABC

from .. import Lattice
from ..crs import Tweak as CRSTweak, Wallpaper
from .dim import Dim, Com, Axis


class Tweak(CRSTweak, ABC):
    """
    Tweak provides the information for clones. It answers the following questions from a clone.
    What is my orientation to the other (self.paper).
    If the other faces West, which direction I should face? face()
    If the other is at dimension 0,0 what cell I be in?  dim()
    Given that the maze might be hollow in the middle, where should I start?
    """

    def __init__(self, paper: Wallpaper, lattice: Lattice, worker_no: int = 0):
        """
        :param paper: The wallpaper being used in the lattice. e.g. Paper.sunset
        :param idx: cube-coord tuple of the offset for the grid centre.
        :param worker_no: The worker number that this paper is identifying with (0..3)
        """
        #
        super().__init__(paper, lattice, worker_no)
        for k in lattice.cells.keys():
            self.coords = k    # cube coords of first valid cell at q=0
            if k != lattice.offset:
                break

    def dim(self, index: tuple) -> Dim:
        # Given a worker number and a master cell, work out which cell the worker should be.
        basis = Dim.adopt(index)
        if self.worker_no == 0:
            return basis
        wx = {
            self.paper.rotate3: Dim.r3,
            self.paper.rotate6: Dim.r6,
            self.paper.sunset: Dim.sunset,
            self.paper.vanity: Dim.vanity,
            self.paper.rotate2: Dim.r2
        }
        return wx[self.paper](basis, self.worker_no)

    def face(self, com: Com) -> [Com, None]:
        if com is None:
            return None
        if self.worker_no != 0:
            if self.paper == self.paper.rotate2:
                return com.opposite
            if self.paper == self.paper.rotate3:
                rcom = com
                for i in range(self.worker_no):
                    rcom = rcom.cw.cw
                return rcom
            if self.paper == self.paper.rotate6:
                rcom = com
                for i in range(self.worker_no):
                    rcom = rcom.cw
                return rcom
            if self.paper == self.paper.sunset:
                offsets = {
                    Com.NN: Com.SS,
                    Com.NE: Com.SE,
                    Com.SE: Com.NE,
                    Com.SS: Com.NN,
                    Com.SW: Com.NW,
                    Com.NW: Com.SW
                }
                return offsets[com]
            if self.paper == self.paper.vanity:
                offsets = {
                    Com.NN: Com.NN,  # √
                    Com.NE: Com.NW,  # √
                    Com.SE: Com.SW,  # √
                    Com.SS: Com.SS,  # √
                    Com.SW: Com.SE,  # √
                    Com.NW: Com.NE  # √
                }
                return offsets[com]
        return com

    def entry(self, border: [int, None]) -> Dim:
        """
        Given that the structure might be hollow, where should an actor start?
        """
        return self.dim(self.coords)

    #    Sunset w1; under (2,3)
    def __repr__(self):
        return str(self.paper) + " w" + str(self.worker_no) + "; under " + str(self.coords)

    #    Sunset w1
    def __str__(self):
        return str(self.paper) + " w" + str(self.worker_no)

