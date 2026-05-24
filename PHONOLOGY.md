# KnotConLang — Phonology

The spoken form of KnotConLang maps each ideogram's six trits to a sequence of consonants and vowels. The written and spoken orderings differ deliberately: the written form interleaves root and case trits to produce a compact visual ideogram; the spoken form separates them, placing the root first so that the semantic content is heard before the grammatical role.

---

## Trit-to-phoneme table

Each trit value maps to a place of articulation; manner of articulation (continuant vs stop) encodes whether the trit is functioning as part of the root or the case.

| Place      | Bilabial | Alveolar | Velar |
|------------|----------|----------|-------|
| **Trit**   | `O`      | `I`      | `X`   |
| **Vowel**  | U        | I        | A     |
| **Continuant** (root consonant) | M | L | Ŋ |
| **Stop** (case consonant)       | P | T | K |

### Vowel sounds

| Vowel | IPA | Sound |
|-------|-----|-------|
| U | [u] | as in *m**oo**n*, *f**oo**d*, *fl**u*** |
| I | [i] | as in *s**ee***, *mach**i**ne*, *k**ee**n* |
| A | [a] | as in *f**a**ther*, *sp**a***, *c**a**r* — an open vowel, not the A of *cat* |

### The Ŋ sound

**Ŋ** (lowercase **ŋ**) is the velar nasal — the *ng* sound in *si**ng***, *ri**ng***, *lo**ng***. 
In English it only appears at the end of syllables, but in Knot ConLang (and 
in Māori, Vietnamese, Yoruba, and many other languages) it occurs freely at the start of a word. 
Pronounce **Ŋumu** by beginning with the *ng* of *singing* and continuing into *oo-moo*. In ASCII contexts, write **NG** in place of **Ŋ**.

- Odd-numbered positions in the spoken sequence → consonant
- Even-numbered positions → vowel
- Root consonant positions use **continuants** (M, L, Ŋ)
- Case consonant positions use **stops** (P, T, K)

---

## Written vs spoken order

The written ideogram format is **CRRCRR** — case and root trits interleaved, one trit per hexagon wall, clockwise from the top:

```
Written position:  1    2    3    4    5    6
Role:              C    R    R    C    R    R
```

For speech, the trits are reordered to **RRRRCC** — all four root trits first, both case trits last:

```
Spoken position:  1    2    3    4    5    6
Source (written): 2    3    5    6    1    4
Role:             R    R    R    R    C    C
Phoneme type:     con  vow  con  vow  con  vow
```

Consonants at positions 1 and 3 (root) use the continuant row.
Consonant at position 5 (case) uses the stop row.
Vowels at positions 2, 4, 6 use the vowel row.

---

## Case suffixes

The nine cases produce these spoken suffixes (case stop + case vowel), subject to elision:

| Case code | Name        | Suffix | Suffix (elided if root ends in same vowel) |
|-----------|-------------|--------|--------------------------------------------|
| `OO`      | abs         | -PU    | -P  (if root trit 4 = O → vowel U)        |
| `OI`      | acc         | -PI    | -P  (if root trit 4 = I → vowel I)        |
| `OX`      | agt         | -PA    | -P  (if root trit 4 = X → vowel A)        |
| `IO`      | gen         | -TU    | -T  (if root trit 4 = O)                  |
| `II`      | loc         | -TI    | -T  (if root trit 4 = I)                  |
| `IX`      | adj         | -TA    | -T  (if root trit 4 = X)                  |
| `XO`      | trn         | -KU    | -K  (if root trit 4 = O)                  |
| `XI`      | int         | -KI    | -K  (if root trit 4 = I)                  |
| `XX`      | nom         | -KA    | -K  (if root trit 4 = X) — or dropped     |

---

## Elision rule

If the final vowel (position 6) is identical to the immediately preceding vowel (position 4), it is dropped.

```
LUŊUPU  →  LUŊUP   (final U matches preceding U — root trit 4 = O, case abs OO)
LUŊIPA  →  LUŊIPA  (final A differs from preceding I — no elision)
```

---

## Nominative

The nominative case (`XX`) need not be spoken. It may be omitted when unambiguous — in ordinary speech the bare root form is understood as nominative. It is retained for disambiguation, formal register, or verse.

A bare root (no case suffix) is four phonemes, (two syllables of CVCV). If 
the nominative would have elided (root trit 4 = X → vowel A = case-nom vowel A), the spoken nominative form is five phonemes ending in K; 
in that case dropping the case suffix is the natural reduction.

---

## Examples

### NAME.abs (`OIOOXO`)

Root index 33 → root trits `IOXO`. Case `abs` → case trits `OO`.

| Step | Result |
|------|--------|
| Written CRRCRR | `O I O O X O` |
| Reorder → RRRRCC | `I O X O O O` |
| Map (root→continuant, case→stop) | L U Ŋ U P U |
| Elide (final U = preceding U) | **LUŊUP** |

### WIND.nom (`OOOIXX`)

Root index 1 → root trits `OOOI` → MULI. 
Case `nom` → case trits `XX` → KA.

| Step | Result |
|------|--------|
| Written CRRCRR | `O O O I X X` |
| Reorder → RRRRCC | `O O I X X X` |
| Map | M U L I K A |
| No elision (A ≠ I) | MULIKA |
| Nominative dropped | **MULI** |

### CAESURA.abs / full stop (`OOOOOO`)

Root index 0 → root trits `OOOO`. Case `abs` → case trits `OO`.

| Step | Result |
|------|--------|
| Written CRRCRR | `O O O O O O` |
| Reorder → RRRRCC | `O O O O O O` |
| Map | M U M U P U |
| Elide (final U = preceding U) | **MUMUP** |

---

## Parsing (spoken → written)

A spoken form is recovered by reversing each step:

1. **Restore elided vowel** — if the word ends in a consonant (5 phonemes), append the vowel at position 4.
2. **Restore dropped nominative** — if only 4 phonemes, append `K A` (case trits `XX`).
3. **Map phonemes to trits** — place of articulation determines trit regardless of manner: M/P → O; L/T → I; Ŋ/K → X; U → O; I → I; A → X.
4. **Reconstruct written order** — spoken positions map back as: (5→C1)(1→R1)(2→R2)(6→C2)(3→R3)(4→R4), giving CRRCRR.

The roundtrip is lossless. A spoken nominative that was dropped is recovered as nominative by default — no information is lost.

---

## Root inventory

All 81 roots, indexed in trit order. 
The four-character trit code encodes the root positions (R1 R2 R3 R4 in spoken order). 
The spoken form shown is the bare root (nominative dropped, no elision applied — that only affects the case suffix).

| #  | Root      | Trits | Spoken |   | #  | Root      | Trits | Spoken |
|----|-----------|-------|--------|---|----|-----------|-------|--------|
|  0 | CAESURA   | OOOO  | MUMU   |   | 41 | MEND      | IIIX  | LILA   |
|  1 | WIND      | OOOI  | MUMI   |   | 42 | FEAR      | IIXO  | LIŊU   |
|  2 | MAN       | OOOX  | MUMA   |   | 43 | FEEL      | IIXI  | LIŊI   |
|  3 | FIRE      | OOIO  | MULU   |   | 44 | HEART     | IIXX  | LIŊA   |
|  4 | ROOT      | OOII  | MULI   |   | 45 | MOUTH     | IXOO  | LAMU   |
|  5 | EYE       | OOIX  | MULA   |   | 46 | MANY      | IXOI  | LAMI   |
|  6 | SIBLING   | OOXO  | MUŊU   |   | 47 | ALIKE     | IXOX  | LAMA   |
|  7 | EAR       | OOXI  | MUŊI   |   | 48 | WAIT      | IXIO  | LALU   |
|  8 | DAY       | OOXX  | MUŊA   |   | 49 | KNOW      | IXII  | LALI   |
|  9 | EARTH     | OIOO  | MIMU   |   | 50 | PRIOR     | IXIX  | LALA   |
| 10 | EDGE      | OIOI  | MIMI   |   | 51 | EAT       | IXXO  | LAŊU   |
| 11 | SELF      | OIOX  | MIMA   |   | 52 | FOOD      | IXXI  | LAŊI   |
| 12 | GROUND    | OIIO  | MILU   |   | 53 | POINT     | IXXX  | LAŊA   |
| 13 | METAL     | OIII  | MILI   |   | 54 | WOMAN     | XOOO  | ŊUMU   |
| 14 | SMALL     | OIIX  | MILA   |   | 55 | LIGHT     | XOOI  | ŊUMI   |
| 15 | WEIGHT    | OIXO  | MIŊU   |   | 56 | REAP      | XOOX  | ŊUMA   |
| 16 | MOVE      | OIXI  | MIŊI   |   | 57 | ONE       | XOIO  | ŊULU   |
| 17 | TIME      | OIXX  | MIŊA   |   | 58 | HIDE      | XOII  | ŊULI   |
| 18 | CHILD     | OXOO  | MAMU   |   | 59 | STRING    | XOIX  | ŊULA   |
| 19 | BODY      | OXOI  | MAMI   |   | 60 | HOLD      | XOXO  | ŊUŊU   |
| 20 | CIRCLE    | OXOX  | MAMA   |   | 61 | VOICE     | XOXI  | ŊUŊI   |
| 21 | FALL      | OXIO  | MALU   |   | 62 | SLEEP     | XOXX  | ŊUŊA   |
| 22 | STRANGER  | OXII  | MALI   |   | 63 | NOSE      | XIOO  | ŊIMU   |
| 23 | MAYBE     | OXIX  | MALA   |   | 64 | HUNT      | XIOI  | ŊIMI   |
| 24 | GIVE      | OXXO  | MAŊU   |   | 65 | LEVEL     | XIOX  | ŊIMA   |
| 25 | MIXED     | OXXI  | MAŊI   |   | 66 | LARGE     | XIIO  | ŊILU   |
| 26 | HAND      | OXXX  | MAŊA   |   | 67 | BREAK     | XIII  | ŊILI   |
| 27 | WATER     | IOOO  | LUMU   |   | 68 | FIELD     | XIIX  | ŊILA   |
| 28 | SKY       | IOOI  | LUMI   |   | 69 | WEAVE     | XIXO  | ŊIŊU   |
| 29 | COLOUR    | IOOX  | LUMA   |   | 70 | NEXT      | XIXI  | ŊIŊI   |
| 30 | BETWEEN   | IOIO  | LULU   |   | 71 | PATH      | XIXX  | ŊIŊA   |
| 31 | ANIMAL    | IOII  | LULI   |   | 72 | NIGHT     | XXOO  | ŊAMU   |
| 32 | HARNESS   | IOIX  | LULA   |   | 73 | SPACE     | XXOI  | ŊAMI   |
| 33 | NAME      | IOXO  | LUŊU   |   | 74 | PLAY      | XXOX  | ŊAMA   |
| 34 | FEW       | IOXI  | LUŊI   |   | 75 | AGE       | XXIO  | ŊALU   |
| 35 | POSITION  | IOXX  | LUŊA   |   | 76 | BREATH    | XXII  | ŊALI   |
| 36 | BONE      | IIOO  | LIMU   |   | 77 | HOUSE     | XXIX  | ŊALA   |
| 37 | WOOD      | IIOI  | LIMI   |   | 78 | WORK      | XXXO  | ŊAŊU   |
| 38 | WATCH     | IIOX  | LIMA   |   | 79 | HERE      | XXXI  | ŊAŊI   |
| 39 | PLANT     | IIIO  | LILU   |   | 80 | MOTHER    | XXXX  | ŊAŊA   |
| 40 | NOT       | IIII  | LILI   |   |    |           |       |        |

Each spoken root is a unique four-phoneme CV·CV sequence. 
The 81 roots cover the full space of bilabial/alveolar/velar combinations in two CV syllables — no two roots sound alike, and no case suffix can be confused with a root boundary since stops only appear in the case position.
