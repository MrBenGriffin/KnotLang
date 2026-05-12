# KnotConLang — How-To

Practical reference for generating knotwork and writing text with `text.py`.

---

## Running

```bash
python text.py [options]
```

Output goes to stdout by default; use `-o FILE` to write to a file. All output is UTF-8 text containing HIBOX ligature codes, renderable with the hex knot fonts.

---

## Options

### Grid shape: `-x {H,T,R,O,E}`

Selects the shape of the hex grid. Default: `H`.

| Code | Shape | Notes |
|------|-------|-------|
| `H` | Hexagon | Regular parallelogram-ish hex grid. `-d` sets columns × rows in axial (q, r) coordinates. |
| `T` | Triangle | Triangular subset of the hex grid. Both `-d` values set the side length. |
| `R` | Rhombus | Dimensions are forced to odd numbers internally. |
| `O` | Odd-column offset | Row count is forced even. Good for text layout. |
| `E` | Even-column offset | Standard even-column offset grid. |

### Grid size: `-d COLS ROWS`

Two integers: columns then rows. Default: `9 9`.

```bash
python text.py -d 20 10        # 20 columns, 10 rows
python text.py -x T -d 8 8    # triangle with side 8
```

**OddMap (`-x O`) ideogram capacity.** Ideograms are placed in odd columns at odd display rows. To fit exactly *X* ideogram columns × *Y* ideogram rows, use:

```
-d (1 + 2X) (2 + 2Y)
```

| Ideogram grid | Dimensions |
|---------------|------------|
| 1 × 1         | `-d 3 4`   |
| 2 × 2         | `-d 5 6`   |
| 3 × 3         | `-d 7 8`   |
| 3 × 4         | `-d 7 10`  |
| 4 × 3         | `-d 9 8`   |

The asymmetry (H = 2 + 2Y vs W = 1 + 2X) exists because odd columns have one fewer row than even columns internally.

### Symmetry: `-s {N,H,V,R2,R3,R6}`

Controls mirror or rotational symmetry. Default: `N`.

| Code | Workers | Description |
|------|---------|-------------|
| `N`  | 1 | No symmetry |
| `H`  | 2 | Mirror on horizontal axis ("sunset") |
| `V`  | 2 | Mirror on vertical axis ("vanity") |
| `R2` | 2 | 180° rotation |
| `R3` | 3 | 120° rotation — grid should be roughly square |
| `R6` | 6 | 60° rotation — grid should be roughly square |

When symmetry is active the grid is mined by multiple workers simultaneously, each operating on its symmetry-transformed copy of the master worker's path. The result is a pattern with that symmetry.

```bash
python text.py -x H -d 12 12 -s R6    # 6-fold rotational symmetry
python text.py -d 15 8 -s H            # horizontal mirror
```

### Tiling: `-t {WE} {NE.SW} {SE.NW}`

Wraps the grid along one or more axes, producing a tileable pattern. Provide axis names as separate arguments.

| Name    | Wraps |
|---------|-------|
| `WE`    | West edge joins east edge |
| `NE.SW` | NE edge joins SW edge |
| `SE.NW` | SE edge joins NW edge |

```bash
python text.py -t WE             # tile horizontally
python text.py -t WE NE.SW       # tile on two axes
```

### Worker: `-w {M,S,F,W}`

The algorithm that mines the grid. Default: `M`.

| Code | Name | Character |
|------|------|-----------|
| `M` | Maze | Depth-first maze carver with random backtracking. Produces flowing, corridor-like knotwork. |
| `S` | Spiral | Generates concentric spiral paths. |
| `F` | Fill | Connects every possible cell. Dense, fully-connected mesh. |
| `W` | Write | Encodes text from `-i` into cells, then fills remaining cells with `F`. |

```bash
python text.py -w F -sb 1.0    # fully-connected straight-line mesh (grid pattern)
python text.py -w S -s R6      # spirals with 6-fold symmetry
```

### Straight/twist balance: `-sb 0.0..1.0`

Controls the ratio of straight passages (`I`) to crossings (`X`). Default: `0.2`.

- `0.0` — all crossings (maximum visual complexity)
- `1.0` — all straights (grid-like, open passages)

```bash
python text.py -sb 0.0    # all twists — dense knotwork
python text.py -sb 1.0    # all straights — maze-like corridors
```

### Space density: `-sp 0.0..1.0`

Controls the probability that any individual wall cut renders as empty space (`O`) rather than a crossing or straight. Default: `0.0` (no spaces).

The space check runs before the straight/twist balance, so `-sp` draws probability from both `X` and `I` equally. Higher values produce a more open, airy background fill.

- `0.0` — no empty spaces (default)
- `0.5` — roughly half the cells appear visually open

```bash
python text.py -sp 0.3           # 30% chance of empty space per wall
python text.py -sp 0.5 -sb 0.5  # half spaces, remainder split evenly between I and X
```

### Connectivity: `-cb 0.0..1.0`

Adjusts how long each corridor runs before backtracking. Default: `0.2`.

Higher values produce fewer, longer threads. Lower values produce more branching.

### Border: `-b N`

Creates a hollow border of thickness N cells around the edge of the grid. The interior is mined normally; the border cells are blocked.

```bash
python text.py -b 2 -d 15 15    # 2-cell border
```

### Random seed: `-r N`

Integer seed for reproducible output. By default a fresh random seed is used each run.

```bash
python text.py -r 42            # always produces the same knot for these parameters
```

### Input file: `-i FILE`

A text file containing words to encode, used with `-w W`. See *Text Input Format* below.

### Output file: `-o FILE`

Write output to a file instead of stdout. The file is UTF-8 text.

---

## Text Input Format

The input file (used with `-w W -i FILE`) contains whitespace-delimited tokens. Each token is one word.

**Format:**

```
ROOT              # nominative case (default)
ROOT.CASE         # explicit case
ROOT_MULTI_WORD   # underscore → space in root name (e.g. TO_BURN → 'TO BURN')
# comment line    # lines beginning with # are ignored
```

**Case abbreviations:** `nom`, `acc`, `gen`, `agt`, `loc`, `adj`, `trn`, `int`, `abs`

**Example file:**

```
# A short statement about knowing
SELF.gen KNOW.nom
NOT.acc CAESURA.adj
KNOW.trn GROUND.nom CAESURA.abs
```

This encodes: "of oneself, knowledge / not- , / to-know the-ground ."

Words that resolve via kenning are expanded automatically. For example, `FISH` expands to `WATER[nom] · ANIMAL[live-case]` — you write `FISH` and the system writes the two ideograms.

If the input exhausts before the grid is full, remaining cells are filled with the normal `F` (Fill) algorithm.

---

## Examples

### Basic knotwork

```bash
# 9×9 hex grid, default settings
python text.py

# Compact rhombus, high connectivity, all twists
python text.py -x R -d 11 11 -cb 0.8 -sb 0.0

# Tileable hex panel
python text.py -x H -d 16 10 -t WE -s H -o panel.txt
```

### Symmetrical designs

```bash
# 3-fold rotation — good for roughly square grids
python text.py -x H -d 10 10 -s R3

# 6-fold rotation — requires roughly square grid
python text.py -x T -d 8 8 -s R6 -sb 0.1

# Horizontal mirror, dense mesh
python text.py -w F -s H -d 14 8
```

### Writing text

Create a file `words.txt`:

```
# Swadesh fragment
WATER FIRE EARTH SKY WIND
GIVE.trn HOLD.trn KNOW.trn
ONE TWO THREE CAESURA.abs
```

Then run:

```bash
python text.py -w W -x O -d 9 12 -i words.txt -o out.txt
```

Open `out.txt` in an editor with the hex knot font active and ligatures enabled.

### Reproducible output

```bash
# Save the seed from a run you liked, then reproduce it
python text.py -r 1234 -x H -d 12 12 -s R2
```

---

## Output Layout

The output is a block of text. Each line represents a row of the offset grid; alternating lines are indented by one space to represent the hex offset. Paste the output into any ligature-capable text renderer with a hex knot font to see the knotwork.

When the Writer (`-w W`) encodes text, odd-column cells at odd display rows carry ideograms. The translation panel beneath the grid lists decoded `[ROOT:case]` pairs grouped by visual row — one line per ideogram row, left-to-right within each row. This layout mirrors the staggered grid, so each translation line corresponds to the visible row of glyphs at the same vertical position. Ideograms are assigned to slots in row-major order (left-to-right, top-to-bottom), matching the translation reading order.
