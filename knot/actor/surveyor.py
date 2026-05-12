from knot.space.hexagonal import Com, Dim
from knot.tool.cut import Cut
from knot.actor import Mover
from knot.space import Lattice
from knot.tool.cutter import Cutter



class Surveyor(Mover):
    """
    Finds points to write text.
    """
    cutoff = 15

    def __init__(self, lattice: Lattice):
        super().__init__(lattice)
        self.track = [self.entrance]
        self.lattice = lattice
        self.tool = Cutter(self.tweak.paper)

    def survey(self):
        sites = []
        addr = set(self.lattice.cells.keys())
        rfx = {Dim.cube_to_odd(q, r, s): (q, r, s) for q, r, s in addr}
        rc = sorted(list(rfx.keys()), key=lambda x:(x[0], -x[1]))
        for ck in rc:  #
            idx = rfx[ck]
            cell = self.lattice.cells[idx]
            walls = cell.walls_that_can_be_doors()
            if len(walls) == 6:
                sites.append(idx)
                for com in [Com.NN, Com.NE, Com.SE, Com.SS, Com.SW, Com.NW]:
                    wall = cell.walls[com]
                    wall.make_door(com, self.tool, Cut.I, force=True)
        for idx in sites:
            cell = self.lattice.cells[idx]
            cell.back_fill()
        return sites


