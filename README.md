# KnotConLang

A hexagonal knotwork generator and constructed-language writing system. It produces HIBOX ligature sequences readable by the hex knot fonts — visual ideograms where the shape of the knot *is* the meaning.

---

## The Fonts

Install one of the fonts from `assets/`:

| File | Weight |
|------|--------|
| `Knots-Hex-Book.ttf` | Regular |
| `Knots-Hex-Light.ttf` | Light |

Enable ligatures in your editor or renderer. With ligatures active, a sequence like `XOOXOO` renders as a single hex knotwork glyph.

---

## Requirements

Python 3.10+. No external dependencies beyond the standard library.

---

## Quick Start

```bash
# Random knotwork, default hexagonal grid
python text.py

# Triangular grid, 6-fold rotational symmetry
python text.py -x T -d 10 10 -s R6

# Full mesh (every cell connected), rhombus grid, tiling east-to-west
python text.py -w F -x R -d 9 9 -t WE

# Write text from a script file
python text.py -w W -x O -d 9 12 -i myscript.txt -o output.txt

# Reproducible output (fixed seed)
python text.py -x H -d 12 8 -s R2 -r 42
```

---

## Documentation

- **[PRIMER.md](PRIMER.md)** — what the system is and how the language works
- **[HOWTO.md](HOWTO.md)** — CLI reference, input format, and worked examples
