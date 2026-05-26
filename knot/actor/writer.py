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
    compact = False

    def __init__(self, lattice: Lattice, setting: Setting):
        super().__init__(lattice)
        self.cut = {'I': Cut.I, 'X': Cut.X, 'O': Cut.O}
        self.select_tool(setting)
        self.track = [self.entrance]
        self.text = []
        self.input_tokens = []
        self.groups = []
        self.lattice = lattice
        self.setting = setting
        self.lexicon = Lexicon()
        self.compact = Writer.compact

    def set_text(self, text):
        self.input_tokens = list(text)
        self.groups = self.lexicon.lex_groups(text)
        self.text = [item for group in self.groups for item in group]

    def _run(self):
        if self.compact and any(len(g) > 1 for g in self.groups):
            self._run_compact()
        else:
            self._run_standard()

    def _run_standard(self):
        survey = self.lattice.survey()
        text = list(self.text)
        n = min(len(text), len(survey))
        coms = [Com.NN, Com.NE, Com.SE, Com.SS, Com.SW, Com.NW]

        for i in range(n):
            cell = self.lattice.cells[survey[i]]
            ideo = text[i]
            if ideo not in self.lexicon.rev:
                print(f'{ideo} not in lexicon')
                continue
            cuts = [self.cut[t] for t in self.lexicon.rev[ideo]]
            for com, cut in zip(coms, cuts):
                cell.walls[com].make_door(com, self.tool, cut, force=True)

        self.text = text[n:]
        # Track remaining input tokens: drop tokens whose group is fully placed;
        # for a partially-placed group, keep the unplaced ideos as inline tokens.
        consumed = n
        kept_tokens = []
        for tok, grp in zip(self.input_tokens, self.groups):
            if consumed >= len(grp):
                consumed -= len(grp)
            elif consumed > 0:
                kept_tokens.extend(grp[consumed:])
                consumed = 0
            else:
                kept_tokens.append(tok)
        self.input_tokens = kept_tokens
        if not self.input_tokens:
            self.groups = []
        fo = Holer(self.lattice, self.setting)
        while not fo.finished:
            fo.run()
        self.finished = True

    def _run_compact(self):
        """Compact placement: stack each kenning's expanded ideographs into
        consecutive cells of a text (odd) column, with caps/boundaries carrying
        the case head/tail trits. Groups pack greedily column-by-column;
        unplaced groups roll over for the next page via input_tokens."""
        coms = [Com.NN, Com.NE, Com.SE, Com.SS, Com.SW, Com.NW]

        cells_by_col = {}
        for coord in self.lattice.cells:
            col, _ = Dim.cube_to_odd(*coord)
            cells_by_col.setdefault(col, []).append(coord)
        text_cols = sorted(c for c in cells_by_col if c & 1)
        col_cells = {col: sorted(cells_by_col[col], key=lambda c: c[2]) for col in text_cols}

        def place_ideogram(coord, ideo):
            cell = self.lattice.cells[coord]
            cuts = [self.cut[t] for t in self.lexicon.rev[ideo]]
            for com, cut in zip(coms, cuts):
                cell.walls[com].make_door(com, self.tool, cut, force=True)

        def place_cap(coord, head_trit=None, tail_trit=None):
            cell = self.lattice.cells[coord]
            if head_trit is not None:
                cell.walls[Com.SS].make_door(Com.SS, self.tool, self.cut[head_trit], force=True)
            if tail_trit is not None:
                cell.walls[Com.NN].make_door(Com.NN, self.tool, self.cut[tail_trit], force=True)
            block_dirs = (Com.NE, Com.SE, Com.SW, Com.NW)
            for com in block_dirs:
                cell.walls[com].block()
            if head_trit is None:
                cell.walls[Com.SS].block()
            if tail_trit is None:
                cell.walls[Com.NN].block()

        placed_text_cells = []
        placed_groups = 0

        if not text_cols:
            return

        col_idx = 0
        ptr = 0
        last_tail = None
        cells_avail = len(col_cells[text_cols[col_idx]])

        def build_plan(group, prior_tail):
            """Build the sequence of cells to place for a group given the
            tail trit of the preceding cell. Returns list of items where
            each is ('cap', head, tail) or ('ideo', ideo, tail)."""
            plan = []
            t = prior_tail
            for i, ideo in enumerate(group):
                key = self.lexicon.rev[ideo]
                head, tail = key[0], key[3]
                # Insert a cap/boundary for the first ideogram of a group, or
                # whenever the adjoining trits would otherwise collide.
                if i == 0 or t != head:
                    plan.append(('cap', head, t))
                plan.append(('ideo', ideo, tail))
                t = tail
            return plan

        for group in self.groups:
            if not group or not all(ideo in self.lexicon.rev for ideo in group):
                placed_groups += 1
                continue

            plan = build_plan(group, last_tail)
            # +1 reserves space for the eventual column tail-cap.
            if ptr + len(plan) + 1 > cells_avail:
                # Close current column with its tail cap.
                if last_tail is not None and ptr < cells_avail:
                    place_cap(col_cells[text_cols[col_idx]][ptr], tail_trit=last_tail)
                    ptr += 1
                col_idx += 1
                if col_idx >= len(text_cols):
                    break
                ptr = 0
                last_tail = None
                cells_avail = len(col_cells[text_cols[col_idx]])
                plan = build_plan(group, last_tail)
                if ptr + len(plan) + 1 > cells_avail:
                    break  # group too tall even for an empty column

            current_cells = col_cells[text_cols[col_idx]]
            for item in plan:
                if item[0] == 'cap':
                    place_cap(current_cells[ptr], head_trit=item[1], tail_trit=item[2])
                else:
                    place_ideogram(current_cells[ptr], item[1])
                    placed_text_cells.append(current_cells[ptr])
                ptr += 1

            last_tail = plan[-1][2]
            placed_groups += 1

        if last_tail is not None and col_idx < len(text_cols):
            current_cells = col_cells[text_cols[col_idx]]
            if ptr < len(current_cells):
                place_cap(current_cells[ptr], tail_trit=last_tail)

        self.lattice.text_cells = placed_text_cells

        # Update remaining for pagination — full unplaced groups roll over.
        self.groups = self.groups[placed_groups:]
        self.input_tokens = self.input_tokens[placed_groups:]
        self.text = [item for grp in self.groups for item in grp]

        # Block NN/SS of reflection cells beside kenning ideographs so the
        # Holer keeps their head/tail trits solid.
        for coord in placed_text_cells:
            cell = self.lattice.cells[coord]
            for com in (Com.NE, Com.SE, Com.NW, Com.SW):
                neighbour = cell.walls[com].cell(com)
                if neighbour is None:
                    continue
                neighbour.walls[Com.NN].block()
                neighbour.walls[Com.SS].block()

        fo = Holer(self.lattice, self.setting)
        while not fo.finished:
            fo.run()
        self.finished = True
