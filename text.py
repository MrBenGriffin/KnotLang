# encoding: utf-8
import os
import random
import argparse

from sympy.physics.units import dimensions

from knot.space.crs import Symmetry
from knot.space.hexagonal import Hexagon, Triangle, Rhombus, OddMap, EvenMap
from knot.works import Structure
from knot.actor import Mazer, Clone, Joiner, Holer, Spiral, Writer
from knot.tool.setting import Setting
from knot.space.hexagonal.lexicon import Lexicon


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


def analyse_groups(expanded: list) -> list[int]:
    """Return display-group sizes matching compact-mode wall logic.

    A group ends when a non-nom (non-punct) word is seen; nom words extend the
    current run and will have their outer foam closed toward the next word.
    Punctuation markers always terminate the current run and are their own group.
    """
    groups = []
    run = 0
    for word, case in expanded:
        if word == '–':
            if run > 0:
                groups.append(run)
                run = 0
            groups.append(1)
        elif case == 'nom':
            run += 1
        else:
            run += 1
            groups.append(run)
            run = 0
    if run > 0:
        groups.append(run)
    return groups


def pack_groups(group_sizes: list, h_cells: int) -> list[list[int]]:
    """Greedy pack groups into columns of `h_cells` available cells each.
    A group of size s adds (s + 2) cells if it's first in a column,
    otherwise (s + 1). The last group's tail cap is the +1 head/+1 tail.
    A column of G groups uses sum(sizes) + G + 1 cells in total."""
    cols = []
    current = []
    current_total = 0
    for s in group_sizes:
        new_total = (s + 2) if not current else (current_total + s + 1)
        if new_total > h_cells:
            if current:
                cols.append(current)
            current = [s]
            current_total = s + 2
        else:
            current.append(s)
            current_total = new_total
    if current:
        cols.append(current)
    return cols


def suggest_dimensions(expanded: list, hex_type: str = 'O', compact: bool = False,
                       groups: list = None, max_cols: int = None) -> list[int]:
    """Suggest OddMap grid dimensions to fit expanded text.

    In compact mode, pack groups (kennings stay contiguous) into multiple text
    columns of a fixed height. `max_cols` caps the page width; remaining groups
    spill onto subsequent pages. Returns [cols, rows] ready for make_knot.
    """
    import math
    n = len(expanded)
    if n == 0:
        return [11, 12]
    if hex_type == 'O':
        if compact:
            sizes = [len(g) for g in groups] if groups is not None else [1] * n
            # Cells per text column = grid_rows - 1 (one row of col-1 is parity-skipped).
            # Pick a column height that fits the largest group (size + 2 caps).
            min_cells = max(sizes) + 2 if sizes else 2
            h_cells = max(12, min_cells)
            cols = pack_groups(sizes, h_cells)
            W = len(cols) if cols else 1
            if max_cols is not None and max_cols > 0:
                W = min(W, max_cols)
            H_grid = h_cells + 1            # grid rows so col-1 has h_cells cells
            if H_grid % 2:
                H_grid += 1
            return [2 * W + 1, H_grid]
        else:
            W = math.ceil(math.sqrt(n))
            H = math.ceil(n / W)
        return [2 * W + 1, 2 * H + 2]
    else:
        W = math.ceil(math.sqrt(n))
        H = math.ceil(n / W)
        return [W, H]


def _parse_tokens(line: str) -> list:
    result = []
    for token in line.partition('#')[0].split():
        if '.' in token:
            root, case = token.split('.', 1)
            if root:
                result.append((root.upper().replace('_', ' '), case.lower()))
        else:
            result.append(token.upper().replace('_', ' '))
    return result


def load_text(path: str) -> list:
    """Parse ROOT or ROOT.CASE tokens from a whitespace-delimited file.
    Underscores in a root become spaces (TO_BURN → 'TO BURN').
    Lines beginning with # are treated as comments. Input is case-insensitive."""
    result = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            result.extend(_parse_tokens(line))
    return result


def _speak_expanded(expanded: list, lex, ascii_mode: bool = False) -> str:
    from knot.space.hexagonal.phonology import pronounce, pronounce_punctuation
    n = len(expanded)
    items = []
    for word, case in expanded:
        is_punct = (word == '–')
        key = lex.rev.get((word, case))
        items.append((key, case, is_punct))

    has_word_after = [False] * n
    for i in range(n - 2, -1, -1):
        if not items[i + 1][2]:
            has_word_after[i] = True
        else:
            has_word_after[i] = has_word_after[i + 1]

    parts = []
    for i, (key, case, is_punct) in enumerate(items):
        if key is None:
            parts.append(f'?({case})?')
            continue
        if is_punct:
            parts.append(pronounce_punctuation(key, ascii=ascii_mode))
        else:
            next_is_punct = (i + 1 < n and items[i + 1][2])
            is_internal = (case == 'nom') and has_word_after[i] and not next_is_punct
            is_terminal = not has_word_after[i] and not next_is_punct
            parts.append(pronounce(key, ascii=ascii_mode, bare=is_internal, terminal=is_terminal))
    return ' '.join(parts)


def interactive_mode():
    from knot.space.hexagonal.lexicon import Lexicon
    from knot.space.hexagonal.phonology import pronounce, pronounce_punctuation
    lex = Lexicon()
    print("KnotConLang — interactive mode  (\\help for commands, Ctrl-D to quit)")
    while True:
        try:
            line = input('\n> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue

        if line.startswith('\\'):
            parts = line[1:].split(None, 1)
            cmd = parts[0].lower()
            rest = parts[1].strip() if len(parts) > 1 else ''

            if cmd in ('quit', 'exit', 'q'):
                break
            elif cmd == 'help':
                print("  WORD.case ...              encode and pronounce a phrase")
                print("  \\add WORD = COMP ...       add a kenning (COMP.case for fixed case)")
                print("  \\list [WORD]               list all kennings or one entry")
                print("  \\find WORD                 kennings that directly use WORD")
                print("  \\rfind WORD                kennings that use WORD (recursive)")
                print("  \\roots                     list all 81 roots with spoken form")
                print("  \\cases                     list all case suffixes")
                print("  \\punctuation               list all punctuation clitics")
                print("  \\quit                      exit")
            elif cmd == 'roots':
                for i, root in enumerate(lex._roots):
                    w_match = '–' if root == 'CAESURA' else root
                    key = next(k for k, (w, c) in lex.roots.items() if w == w_match)
                    spoken = pronounce(key, bare=True)
                    print(f"  {i:2}  {root:<12}  {spoken}")
            elif cmd == 'cases':
                for code, name in lex.cases.items():
                    full = lex._cases.get(name, name)
                    # build a sample suffix from code
                    from knot.space.hexagonal.phonology import _STOP, _VOW
                    suffix = _STOP[code[0]] + _VOW[code[1]]
                    print(f"  {name:<4}  -{suffix}   {full}")
            elif cmd == 'punctuation' or cmd == 'punct':
                from knot.space.hexagonal.phonology import _STOP, _VOW
                for code, symbol in lex._particles.items():
                    name = lex.cases[code]
                    clitic = _STOP[code[0]] + _VOW[code[1]]
                    docs = lex._particle_docs.get(code, '')
                    print(f"  {symbol}   {name:<4}  spoken: {clitic}; {docs}")
            elif cmd == 'add':
                if '=' not in rest:
                    print("  usage: \\add WORD = COMPONENT1 COMPONENT2.case ...")
                    continue
                word, _, comps_str = rest.partition('=')
                word = word.strip().upper()
                components = []
                for comp in comps_str.split():
                    if '.' in comp:
                        r, c = comp.split('.', 1)
                        components.append((r.upper(), c.lower()))
                    else:
                        components.append(comp.upper())
                lex.save_kenning(word, components)
                comp_str = ' '.join(f'{c[0]}.{c[1]}' if isinstance(c, tuple) else c for c in components)
                print(f"  saved: {word} = {comp_str}")
            elif cmd == 'list':
                target = rest.upper() if rest else None
                if target:
                    if target in lex.kennings:
                        comps = lex.kennings[target]
                        comp_str = ' '.join(f'{c[0]}.{c[1]}' if isinstance(c, tuple) else c for c in comps)
                        print(f"  {target} = {comp_str}")
                    else:
                        print(f"  '{target}' not in kennings")
                else:
                    for k in sorted(lex.kennings):
                        comps = lex.kennings[k]
                        comp_str = ' '.join(f'{c[0]}.{c[1]}' if isinstance(c, tuple) else c for c in comps)
                        print(f"  {k} = {comp_str}")
            elif cmd in ('find', 'rfind'):
                target = rest.upper()
                if not target:
                    print(f"  usage: \\{cmd} WORD")
                    continue

                def _comp_name(comp):
                    return comp[0].upper() if isinstance(comp, tuple) else comp.upper()

                def _direct_users(word):
                    return {k for k, comps in lex.kennings.items()
                            if any(_comp_name(c) == word for c in comps)}

                if cmd == 'find':
                    found = _direct_users(target)
                else:
                    found = set()
                    frontier = {target}
                    while frontier:
                        new = set()
                        for word in frontier:
                            new |= _direct_users(word) - found
                        found |= new
                        frontier = new

                if found:
                    for k in sorted(found):
                        comps = lex.kennings[k]
                        comp_str = ' '.join(f'{c[0]}.{c[1]}' if isinstance(c, tuple) else c for c in comps)
                        print(f"  {k} = {comp_str}")
                else:
                    print(f"  '{target}' not used in any kenning")
            else:
                print(f"  unknown command: \\{cmd}  (try \\help)")
        else:
            tokens = _parse_tokens(line)
            if not tokens:
                continue
            try:
                expanded = lex.lex(tokens)
                decoded = ' '.join(f'{w}.{c}' if w != '–' else c for w, c in expanded)
                keys = ' '.join(lex.rev.get((w, c), '??????') for w, c in expanded)
                spoken = _speak_expanded(expanded, lex)
                print(f"  decoded: {decoded}")
                print(f"  keys:    {keys}")
                print(f"  spoken:  {spoken}")
            except Exception as e:
                print(f"  error: {e}")


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
    Writer.compact = args.get('compact', False)
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
    if isinstance(master, Writer):
        remaining = master.input_tokens if master.compact else master.text
    else:
        remaining = []
    read_text = knot_work.lattice.decode() if translate else ''
    spoken_text = knot_work.lattice.speak() if translate else ''
    return knot_work.lattice.code(), read_text, spoken_text, remaining

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
    parser.add_argument("-d", "--dimensions", nargs='+', type=int, default=None,
                        help="Grid dimensions: columns then rows. Auto-computed from text when omitted.")
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
    parser.add_argument("-I", "--interactive", action="store_true",
                        help="Enter interactive mode for encoding/pronouncing phrases.")
    parser.add_argument("-C", "--compact", action="store_true",
                        help="Compact kenning compounds: close outer foam between adjacent nom-case ideographs.")
    return parser


if __name__ == "__main__":
    import sys
    # 62
    x, y = 7, 9
    xy = [(1 + 2 * x), (2 + 2 * y)]
    args = sys.argv[1:] or dict_to_argv({"input": 'beowulf.txt', "spaces": 0.0, "straights": 0.0, "dimensions": xy,
                                         "connectivity": 0.99, "border": 0, "worker": "W", #  "compact": None,
                                         "interactive": None, "symmetry": "N", "hex": "O", "translate": 1})
    parser = build_arg_parser()
    arg_dict = vars(parser.parse_args(args))
    if arg_dict.get('interactive'):
        interactive_mode()
        sys.exit(0)
    translate = arg_dict['translate'] == 1
    workers = {'M': Mazer, 'S': Spiral, 'F': Holer, 'W': Writer}
    arg_dict['worker'] = workers[arg_dict['worker']]
    text = load_text(arg_dict['input']) if arg_dict.get('input') else []
    expanded = []
    if text:
        lexicon = Lexicon()
        expanded = lexicon.lex(text)
        print(f"Loaded {len(expanded)} ideographs from text")
    if arg_dict['dimensions'] is None:
        if arg_dict['worker'] is Writer and expanded:
            compact = arg_dict.get('compact', False)
            hex_type = arg_dict.get('hex', 'O')
            groups_for_dims = lexicon.lex_groups(text) if (text and compact) else None
            arg_dict['dimensions'] = suggest_dimensions(
                expanded, hex_type=hex_type, compact=compact, groups=groups_for_dims)
            cols, rows = arg_dict['dimensions']
            W = (cols - 1) // 2
            H = (rows - 2) // 2
            if compact:
                sizes = [len(g) for g in groups_for_dims] if groups_for_dims else [1] * len(expanded)
                packed = pack_groups(sizes, rows - 1)
                print(f"Auto dimensions (compact): {cols}×{rows} → {W} text cols × {rows-1} cells/col"
                      f"  [groups: {len(sizes)}, max: {max(sizes)}, packs into {len(packed)} cols]")
            else:
                print(f"Auto dimensions: {cols}×{rows} → {W}×{H} text cells")
        else:
            arg_dict['dimensions'] = [9, 9]
    seed = arg_dict['random']
    remaining = text
    pages = []
    texts = []
    spoken = []
    page = 0
    while True:
        page_args = dict(arg_dict)
        if isinstance(seed, int):
            page_args['random'] = seed + page
        elif page > 0:
            page_args['random'] = os.urandom(7)
        code, read_text, spoken_text, next_remaining = make_knot(page_args, remaining, translate=translate)
        pages.append(code)
        texts.append(read_text)
        spoken.append(spoken_text)
        if not next_remaining or next_remaining == remaining:
            break
        remaining = next_remaining
        page += 1
    result = ''.join(pages)
    result += '\n' + (''.join(texts))
    if translate:
        result += '\n' + (' '.join(spoken))
    if arg_dict.get('output'):
        with open(arg_dict['output'], 'w', encoding='utf-8') as f:
            f.write(result)
    else:
        print(result, end='')
