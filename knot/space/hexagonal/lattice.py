# encoding: utf-8
from abc import abstractmethod
from ..lattice import Lattice as CRSLattice
from .dim import Dim, Axis
from ..cell import Cell
from ..wall import Wall

"""
cf. https://www.redblobgames.com/grids/hexagons/
    https://www.redblobgames.com/grids/hexagons/implementation.html
"""


class Lattice(CRSLattice):

    def __init__(self, crs, size, tiling=None):
        super().__init__(crs, size, tiling)
        self.text_cells = self.survey()

    def survey(self):
        from knot.actor.surveyor import Surveyor
        self.text_cells = Surveyor(self).survey()
        return self.text_cells


    def set_range(self):
        # set_range provides min/max values for cells in each axis.
        vals = []
        for a in self.axes:
            v = self.size[a]
            if isinstance(v, tuple):
                vals.append((v[0], v[1]) if self.wrap[a] else (v[0], v[1] + 1))
            else:
                vals.append(v + 1)
        return self.dim.adopt(tuple(vals))

    @abstractmethod
    def set_cells(self) -> dict:
        pass

    def do_walls(self, wall_dims, cell_coords) -> dict:
        walls = dict((a, dict()) for a in self.axes)
        cells = dict()

        bas = [0 for _ in self.axes]
        cnt = [set() for _ in self.axes]
        n = len(cell_coords)
        a = len(self.axes)
        for cell in cell_coords:
            for i in range(a):
                bas[i] += cell[i]
                cnt[i].add(cell[i])
        rfn = [b / n for b in bas]
        ctr = [b // n for b in bas]
        self.offset = tuple(ctr)
        for c in cell_coords:
            cell_walls = {}
            dim = self.dim(*c)
            for a in self.axes:
                for pole in (a.a, a.b):
                    wall = dim.edge(pole, wall_dims, self.wrap)
                    if wall:
                        wt = wall.tuple()
                        if wt not in walls[a]:
                            walls[a][wt] = Wall()
                        cell_walls[pole] = walls[a][wt]
            cells[c] = Cell(dim, cell_walls)
        return cells

    def code(self):
        result = "\n"
        min_q = self.min(Axis.W___E.idx)
        min_r = self.min(Axis.NE_SW.idx)
        max_q = self.max(Axis.W___E.idx)
        max_r = self.max(Axis.NE_SW.idx)
        if min_q % 2 == 0:
            r_t_base = ""
            r_b_base = " "
        else:
            r_t_base = " "
            r_b_base = ""
        # odd-q offset: col is the offset-col, row is the offset-row
        min_parity = min_q & 1
        min_col = min_q
        min_row = min_r + (min_q - min_parity) // 2
        max_parity = max_q & 1
        max_col = max_q
        max_row = max_r + (max_q - max_parity) // 2
        for row in range(min_row, max_row + 1):
            r_t = r_t_base
            r_b = r_b_base
            for col in range(min_col, max_col + 1):
                tup = Dim.odd_to_cube(col, row)
                cell = "  "
                cell_obj = self.cells.get(tup)
                if cell_obj is not None:
                    cell = cell_obj.code()
                if col % 2 == 0:
                    r_t += cell
                else:
                    r_b += cell
            result += r_t.rstrip() + "\n" + r_b.rstrip() + "\n"
        return result


    def decode(self):
        from .lexicon import Lexicon
        lex = Lexicon()
        result = ""
        for idx in self.text_cells:
            cell = self.cells[idx].code()
            if cell == '  ':
                cell = 'OOOOOO'
            lex_rt, lex_case = lex.roots[cell]
            result += f' {lex_rt}.{lex_case}'
        return result

    def speak(self, ascii_mode: bool = False) -> str:
        from .lexicon import Lexicon
        from .phonology import pronounce, pronounce_punctuation
        lex = Lexicon()

        # Collect (cell_key, is_punct) for all text cells
        items = []
        for idx in self.text_cells:
            cell = self.cells[idx].code()
            if cell == '  ':
                cell = 'OOOOOO'
            lex_rt, lex_case = lex.roots[cell]
            items.append((cell, lex_case, lex_rt == '–'))

        # Precompute lookahead: does a non-punct word follow position i?
        n = len(items)
        has_word_after = [False] * n
        for i in range(n - 2, -1, -1):
            if not items[i + 1][2]:
                has_word_after[i] = True
            else:
                has_word_after[i] = has_word_after[i + 1]

        parts = []
        for i, (cell, lex_case, is_punct) in enumerate(items):
            if is_punct:
                # Punctuation clitics: speak only the case syllable (stop + vowel)
                parts.append(pronounce_punctuation(cell, ascii=ascii_mode))
            else:
                next_is_punct = (i + 1 < n and items[i + 1][2])
                # Nom word mid-sequence (not immediately before punct) = compound internal
                is_internal = (lex_case == 'nom') and has_word_after[i] and not next_is_punct
                # True utterance end: no following words and no following punct clitic
                is_terminal = not has_word_after[i] and not next_is_punct
                parts.append(pronounce(cell, ascii=ascii_mode, bare=is_internal, terminal=is_terminal))

        return ' '.join(parts)
