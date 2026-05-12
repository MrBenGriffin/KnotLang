# encoding: utf-8
import os
import random
import argparse

from knot.space.crs import Symmetry
from knot.space.hexagonal import Hexagon, Triangle, Rhombus, OddMap, EvenMap
from knot.works import Structure
from knot.actor import Mazer, Clone, Joiner, Holer, Spiral, Writer
from knot.tool.setting import Setting


# This is used for argument passing
class ArgRange(object):
    from decimal import Decimal
    huge = Decimal('+infinity')
    huge_str = '{:.4E}'.format(huge)

    def __init__(self, start, stop=huge, n=3):
        self.start = start
        self.stop = stop
        self.n = n

    def __contains__(self, key):
        return self.start <= key <= self.stop

    def __iter__(self):
        if self.stop < self.start + (self.n * 3):
            if isinstance(self.stop, int):
                for i in range(self.start, self.stop):
                    yield i
            else:
                yield self.start
        else:
            if isinstance(self.stop, int):
                for i in range(self.start, self.start + self.n):
                    yield i
            if self.stop is self.huge:
                yield '...' + self.huge_str
            else:
                yield '...'
                if isinstance(self.stop, int):
                    for i in range(self.stop - self.n, self.stop):
                        yield i
                else:
                    yield self.stop


def load_text(path: str) -> list:
    """Parse ROOT or ROOT.CASE tokens from a whitespace-delimited file.
    Underscores in a root become spaces (TO_BURN → 'TO BURN').
    Lines beginning with # are treated as comments."""
    result = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.partition('#')[0]
            for token in line.split():
                if '.' in token:
                    root, case = token.split('.', 1)
                    result.append((root.replace('_', ' '), case))
                else:
                    result.append(token.replace('_', ' '))
    return result


def make_knot(args: dict, text: list = None, translate: bool = True) -> tuple:
    random.seed(args['random'])
    shapes = {
        "H": Hexagon,
        "T": Triangle,
        "R": Rhombus,
        "O": OddMap,
        "E": EvenMap,
    }
    shape = shapes.get(args['hex'], Hexagon)()
    style = shape.paper().select(args['symmetry'])
    if style is None:
        style = shape.paper().identity()
    dims = args['dimensions']
    if args['hex'] == 'R':
        dims = [1 + 2 * (d // 2) for d in dims]
    elif args['hex'] == 'O':
        dims = [dims[0], 2 * (dims[1] // 2)]
    knot_work = Structure(shape, dims, args['border'], args['tiling'])
    setting = Setting(args['straights'], spaces_balance=args['spaces'])
    Mazer.cutoff = int(20.0 * args['connectivity'])
    Holer.balance = args['connectivity']
    master = args['worker'](knot_work.lattice, setting)
    if isinstance(master, Writer):
        master.set_text(text or [])
    knot_work.add_bod(master)
    for w in range(1, style.workers):
        clone = Clone(knot_work.lattice, master, style, w)
        knot_work.add_bod(clone)
    knot_work.mine()
    if len(knot_work.bods) > 1:
        knot_work.bods.clear()
        joiner = Joiner(knot_work.lattice, master)
        knot_work.add_bod(joiner)
        for w in range(1, style.workers):
            clone = Clone(knot_work.lattice, joiner, style, w)
            knot_work.add_bod(clone)
        knot_work.join()
    remaining = master.text if isinstance(master, Writer) else []
    read_text = knot_work.lattice.decode() if translate else ''
    return knot_work.lattice.code(), read_text, remaining

def dict_to_argv(d):
    argv = []
    for k, v in d.items():
        argv.append(f"--{k}")
        if v is None:
            continue
        if isinstance(v, list):
            argv.extend(str(x) for x in v)  # NOT join
        else:
            argv.append(str(v))
    return argv


def build_arg_parser():
    balance = ArgRange(0.0, 1.0)
    epilog = """
  Shape (-x):
    H  Regular hex grid. -d sets columns x rows in axial (q, r) coordinates.
    T  Triangular subset of the hex grid (both -d values set the side length).
    R  Rhombus grid (dimensions forced to odd).
    O  Odd-column offset grid.
    E  Even-column offset grid.

  Symmetry (-s):
      N   No symmetry (single pass).
      H   Mirror on the horizontal axis (sunset symmetry).
      V   Mirror on the vertical axis (vanity symmetry).
      R2  180-degree rotation (two workers).
      R3  120-degree rotation (three workers, grid should be square).
      R6  60-degree rotation  (six workers, grid should be square).

  Tiling (-t):
      WE      Wrap west-to-east.
      NE.SW   Wrap northeast-to-southwest.
      SE.NW   Wrap southeast-to-northwest.
    Example: -t WE NE.SW

  Text input (-i):
    Whitespace-delimited file of ROOT or ROOT.CASE tokens.
    Underscores substitute spaces in multi-word roots (e.g. TO_BURN).
    Lines beginning with # are ignored.
    Example:  SELF.gen KNOW.nom NOT.acc CAESURA.adj

  Output: two-letter HIBOX ligature codes for the hex knot font.
    Use -o to write to a file instead of stdout.
"""
    parser = argparse.ArgumentParser(
        description="Generate hexagonal knotwork as HIBOX ligature output for the hex knot font.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-d", "--dimensions", nargs='+', type=int, default=[9, 9],
                        help="Grid dimensions: columns then rows. (default: %(default)s)")
    parser.add_argument("-t", "--tiling", nargs='+', type=str, default=[],
                        help="Tiling (wrapping) axes: WE, NE.SW, SE.NW.")
    parser.add_argument("-s", "--symmetry", type=str, default='N', choices=Symmetry.choices(),
                        help="N/H/V/R2/R3/R6 symmetry mode. (default: %(default)s)")
    parser.add_argument("-b", "--border", type=int,
                        help="Border thickness (default: none).")
    parser.add_argument("-w", "--worker", type=str, default='M', choices=['M', 'S', 'F', 'W'],
                        help="M=Maze, S=Spiral, F=Fill, W=Write. (default: %(default)s)")
    parser.add_argument("-sb", "--straights", type=float, default=0.2, choices=balance,
                        help="Straight/twist balance: 0.0=all twists, 1.0=all straights. (default: %(default)s)")
    parser.add_argument("-sp", "--spaces", type=float, default=0.0, choices=balance,
                        help="Space density: probability of an empty cell. (default: %(default)s)")
    parser.add_argument("-x", "--hex", type=str, choices=['H', 'T', 'R', 'O', 'E'], default='H',
                        help="Grid shape: H=Hexagon, T=Triangle, R=Rhombus, O=Odd, E=Even. (default: %(default)s)")
    parser.add_argument("-cb", "--connectivity", type=float, default=0.2, choices=balance,
                        help="Connection density: larger = longer threads. (default: %(default)s)")
    parser.add_argument("-r", "--random", type=int, default=os.urandom(7),
                        help="Random seed for reproducible output. (default: os.urandom)")
    parser.add_argument("-i", "--input", type=str, metavar='FILE',
                        help="Text input file: whitespace-delimited ROOT or ROOT.CASE tokens.")
    parser.add_argument("-T", "--translate", type=int, default=0, choices=[0, 1],
                        help="Translate lattice (and output).")
    parser.add_argument("-o", "--output", type=str, metavar='FILE',
                        help="Write output to FILE instead of stdout.")
    return parser


if __name__ == "__main__":
    import sys
    x, y = 3, 3
    args = sys.argv[1:] or dict_to_argv({"input": 'man_woman.txt', "spaces": 0.0, "straights": 0.0, "dimensions": [(1+2*x), (2+2*y)], "connectivity": 0.9,
                                         "border": 0, "worker": "W", "symmetry": "N", "hex": "H", "translate": 1})
    parser = build_arg_parser()
    arg_dict = vars(parser.parse_args(args))
    translate = arg_dict['translate'] == 1
    workers = {'M': Mazer, 'S': Spiral, 'F': Holer, 'W': Writer}
    arg_dict['worker'] = workers[arg_dict['worker']]
    text = load_text(arg_dict['input']) if arg_dict.get('input') else []
    seed = arg_dict['random']
    remaining = text
    pages = []
    texts = []
    page = 0
    while True:
        page_args = dict(arg_dict)
        if isinstance(seed, int):
            page_args['random'] = seed + page
        elif page > 0:
            page_args['random'] = os.urandom(7)
        code, read_text, next_remaining = make_knot(page_args, remaining, translate=translate)
        pages.append(code)
        texts.append(read_text)
        if not next_remaining or next_remaining == remaining:
            break
        remaining = next_remaining
        page += 1
    result = ''.join(pages)
    result += '\n' + (''.join(texts))
    if arg_dict.get('output'):
        with open(arg_dict['output'], 'w', encoding='utf-8') as f:
            f.write(result)
    else:
        print(result, end='')
