from knot.space.hexagonal import Com, Dim
from knot.tool.cut import Cut
from knot.actor import Holer, Mover
from knot.space import Lattice
from knot.tool.setting import Setting
from knot.space.hexagonal.lexicon import Lexicon


class Writer(Mover):
    """
    Writes text.
    """
    cutoff = 15

    def __init__(self, lattice: Lattice, setting: Setting):
        super().__init__(lattice)
        self.cut = {'I': Cut.I, 'X': Cut.X, 'O': Cut.O}
        self.select_tool(setting)
        self.track = [self.entrance]
        self.text = []
        self.lattice = lattice
        self.setting = setting
        self.lexicon = Lexicon()

    def _run(self):
        survey = self.lattice.survey()
        for idx in survey:
            if not self.text:
                break
            cell = self.lattice.cells[idx]
            ideo, self.text = self.text[0], self.text[1:]
            if ideo not in self.lexicon.rev:
                print(f'{ideo} not in lexicon')
                continue
            ideogram = self.lexicon.rev[ideo]
            cuts = [self.cut[i] for i in ideogram]
            coms = [Com.NN, Com.NE, Com.SE, Com.SS, Com.SW, Com.NW]
            for com, cut in zip(coms, cuts):
                wall = cell.walls[com]
                wall.make_door(com, self.tool, cut, force=True)
        fo = Holer(self.lattice, self.setting)
        while not fo.finished:
            fo.run()
        self.finished = True

    def set_text(self, text):
        self.text = self.lexicon.lex(text)


