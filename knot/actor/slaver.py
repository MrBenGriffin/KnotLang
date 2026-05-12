import random
from .mover import Mover
from ..space import Lattice
from ..tool import Setting


class Slaver(Mover):
    """
    An alternative (hybrid) to the Miner/Lister.
    This is because lister gives lots of single-cell corridors * yuck *
        (1) Act like the Miner for 16 (or 32) turns.
        (2) Act like the Lister for 1 turn.
    """

    def __init__(self, lattice: Lattice, setting: Setting):
        super().__init__(lattice)
        self.sequence = 0
        self.seq_mod = 5
        self.cell_index = None
        self.faces = []
        self.select_tool(setting)
        self.dig(self.entrance)


    def _run(self):
        self.sequence += 1
        the_wall = None
        while self.track and the_wall is None:
            if self.sequence & self.seq_mod != 0:   # cheaper than % 16  (22 was interesting, 15/16 was default)
                this_cell = self.cell()
                if not self.work(this_cell):
                    self.track.pop()
            else:
                self.forward = 0
                cell_index = random.randrange(len(self.track))
                this_cell = self.track[cell_index]
                if not self.work(this_cell):
                    del self.track[cell_index]

    def work(self, cell) -> bool:
        walls = cell.walls_that_can_be_dug()
        if walls:
            face = random.choice(walls)
            wall = cell.walls[face]
            next_cell = wall.make_door(face, self.tool)
            self.go(next_cell)
            self.face = face.opposite
            return True
        else:
            return False
