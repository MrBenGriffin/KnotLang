# encoding: utf-8
"""
Phonological encoding and decoding for KnotConLang ideograms.

Each 6-trit ideogram key (CRRCRR written order) maps to a spoken form:
  1. Reorder to RRRRCC  (root trits first, case trits last)
  2. Odd positions → consonant; even positions → vowel
  3. Root consonants use continuants (M / L / Ŋ); case consonants use stops (P / T / K)
  4. Elide final vowel if identical to the preceding vowel (position 6 == position 4)
  5. Nominative (XX) may be dropped; a bare 4-phoneme form is read as nominative on parse.
  6. Terminal vowel elision: at a true utterance boundary, the final vowel is dropped.
     This is suspended before punctuation clitics (use pronounce with terminal=False).
  7. Compounds: internal morphemes appear in bare root form (bare=True, 4 phonemes).
  8. Punctuation: only the case syllable (stop + vowel) is spoken; use pronounce_punctuation.
"""

_CON  = {'O': 'M',  'I': 'L',  'X': 'Ŋ'}
_CON_ASCII = {'O': 'M', 'I': 'L', 'X': 'NG'}
_STOP = {'O': 'P',  'I': 'T',  'X': 'K'}
_VOW  = {'O': 'U',  'I': 'I',  'X': 'A'}
_VOWELS = frozenset(_VOW.values())

# Place of articulation → trit (same mapping for consonants and vowels)
_TRIT = {
    'M': 'O', 'P': 'O', 'U': 'O',
    'L': 'I', 'T': 'I', 'I': 'I',
    'Ŋ': 'X', 'K': 'X', 'A': 'X',
}


def pronounce(key: str, ascii: bool = False, bare: bool = False, terminal: bool = False) -> str:
    """Convert a 6-trit ideogram key (CRRCRR) to its spoken form.

    ascii=True    — replaces Ŋ with NG.
    bare=True     — return the 4-phoneme root only; for internal compound elements
                    where the nominative is always dropped.
    terminal=True — apply terminal vowel elision (utterance-final position).
                    Must be False when the word is followed by a punctuation clitic.
    """
    c1, r1, r2, c2, r3, r4 = key[0], key[1], key[2], key[3], key[4], key[5]
    con = _CON_ASCII if ascii else _CON
    phonemes = [
        con[r1],    # spoken pos 1: root consonant (continuant)
        _VOW[r2],   # spoken pos 2: vowel
        con[r3],    # spoken pos 3: root consonant (continuant)
        _VOW[r4],   # spoken pos 4: vowel
        _STOP[c1],  # spoken pos 5: case consonant (stop)
        _VOW[c2],   # spoken pos 6: vowel
    ]
    if bare:
        return ''.join(phonemes[:4])
    if phonemes[5] == phonemes[3]:
        phonemes = phonemes[:5]
    result = ''.join(phonemes)
    if terminal and result[-1] in _VOWELS:
        result = result[:-1]
    return result


def pronounce_punctuation(key: str, ascii: bool = False) -> str:
    """Return the spoken form of a punctuation clitic: case stop + case vowel only.

    Punctuation markers (CAESURA words) are prosodic clitics. Only the final
    syllable — the case consonant and its vowel — is spoken. No elision applies.
    The preceding word retains its final vowel (terminal elision suspended).

    Examples: ∴ (trn, XO) → KU;  ? (nom, XX) → KA;  . (abs, OO) → PU
    """
    con = _CON_ASCII if ascii else _CON
    c1, c2 = key[0], key[3]
    return _STOP[c1] + _VOW[c2]


def _tokenize(spoken: str) -> list:
    """Split spoken form into phoneme tokens; NG (any case) → Ŋ."""
    tokens = []
    i = 0
    while i < len(spoken):
        ch = spoken[i]
        if ch in 'nN' and i + 1 < len(spoken) and spoken[i + 1] in 'gG':
            tokens.append('Ŋ')
            i += 2
        else:
            tokens.append(ch.upper())
            i += 1
    # normalise lowercase eng
    return ['Ŋ' if t == 'ŋ'.upper() else t for t in tokens]


def parse(spoken: str) -> str:
    """Convert a spoken form back to a 6-trit ideogram key (CRRCRR).

    Handles elided final vowel (5 phonemes) and dropped nominative (4 phonemes).
    Raises ValueError for unrecognised phoneme counts or unknown phonemes.
    """
    tokens = _tokenize(spoken)
    n = len(tokens)
    if n == 4:
        tokens = tokens + ['K', 'A']       # restore dropped nominative (XX)
    elif n == 5:
        tokens = tokens + [tokens[3]]      # restore elided final vowel
    elif n != 6:
        raise ValueError(f"Cannot parse '{spoken}': expected 4–6 phonemes, got {n}")

    try:
        r1, r2, r3, r4, c1, c2 = (_TRIT[t] for t in tokens)
    except KeyError as e:
        raise ValueError(f"Unknown phoneme {e} in '{spoken}'") from None

    return c1 + r1 + r2 + c2 + r3 + r4
