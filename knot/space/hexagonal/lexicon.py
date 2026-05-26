# from ..cell import Cell
# from dim import Dim
import os

_KENNINGS_FILE = os.path.join(os.path.dirname(__file__), 'kennings.txt')


class Lexicon:
    def __init__(self):
        self.kennings = self._load_kennings()
        self._init_roots()

    def _load_kennings(self) -> dict:
        kennings = {}
        if not os.path.exists(_KENNINGS_FILE):
            return kennings
        with open(_KENNINGS_FILE, encoding='utf-8') as f:
            for line in f:
                line = line.partition('#')[0].strip()
                if not line or '=' not in line:
                    continue
                word, _, comps_str = line.partition('=')
                word = word.strip().upper()
                components = []
                for comp in comps_str.split():
                    if '.' in comp:
                        root, case = comp.split('.', 1)
                        components.append((root.upper(), case))
                    else:
                        components.append(comp.upper())
                kennings[word] = components
        return kennings

    def save_kenning(self, word: str, components: list):
        word = word.upper()
        self.kennings[word] = components
        parts = []
        for comp in components:
            if isinstance(comp, tuple):
                parts.append(f'{comp[0].upper()}.{comp[1]}')
            else:
                parts.append(comp.upper())
        with open(_KENNINGS_FILE, 'a', encoding='utf-8') as f:
            f.write(f'{word} = {" ".join(parts)}\n')

    def _init_roots(self):
        self._roots = [
            'CAESURA',
            'WIND', 'MAN', 'FIRE', 'ROOT', 'EYE', 'SIBLING', 'EAR', 'DAY', 'EARTH',
            'EDGE', 'SELF', 'GROUND', 'METAL', 'SMALL', 'WEIGHT', 'MOVE', 'TIME', 'CHILD',
            'BODY', 'CIRCLE', 'FALL', 'STRANGER', 'MAYBE', 'GIVE', 'MIXED', 'HAND', 'WATER',
            'SKY', 'COLOUR', 'BETWEEN', 'ANIMAL', 'HARNESS', 'NAME', 'FEW', 'POSITION', 'BONE',
            'WOOD', 'WATCH', 'PLANT', 'NOT', 'MEND', 'FEAR', 'FEEL', 'HEART', 'MOUTH',
            'MANY', 'ALIKE', 'WAIT', 'KNOW', 'PRIOR', 'EAT', 'FOOD', 'POINT', 'WOMAN',
            'LIGHT', 'REAP', 'ONE', 'HIDE', 'STRING', 'HOLD', 'VOICE', 'SLEEP', 'NOSE',
            'HUNT', 'LEVEL', 'LARGE', 'BREAK', 'FIELD', 'WEAVE', 'NEXT', 'PATH', 'NIGHT',
            'SPACE', 'PLAY', 'AGE', 'BREATH', 'HOUSE', 'WORK', 'HERE', 'MOTHER'
        ]
        self._cases = {
            'abs': 'abstract',
            'gen': 'genitive',
            'agt': 'agentive',
            'acc': 'accusative',
            'loc': 'locative',
            'adj': 'adjective',
            'trn': 'transitive',
            'inv': 'intransitive',
            'nom': 'nominative',
        }
        self.cases = {
            'OO': 'abs',  # abstract
            'OI': 'acc',  # accusative
            'OX': 'agt',  # agentive
            'IO': 'gen',  # genitive
            'II': 'loc',  # locative
            'IX': 'adj',  # adjective
            'XO': 'trn',  # transitive
            'XI': 'int',  # intransitive
            'XX': 'nom',  # nominative
        }
        self._particles = {
            'OO': '.',  # 'abs' = full stop', 'end of statement
            'OI': '’',  # 'acc' = closer - "is what was said"
            'OX': '→',  # 'agt'= if/when / conditional / at which point
            'IO': '‘',  # 'gen' = opener — "she said:... "
            'II': ':',  # 'loc' = in other words / that is to say / zoom-in
            'IX': ',',  # 'adj' = also / unordered / items of equal weight
            'XO': '∴',  # 'trn'= causal break — "because / therefore / then"
            'XI': ';',  # 'int' = first / then / ordered / items of ranked weight
            'XX': '?',  # 'nom' = interrogative / '?'
        }
        self._particle_docs = {
            'OO': 'full stop, end of statement',
            'OI': 'closer - "is what was said"',
            'OX': 'if/when / conditional / at which point',
            'IO': 'opener — "she said:... "',
            'II': 'in other words / that is to say / zoom-in',
            'IX': 'also / unordered / items of equal weight',
            'XO': 'causal break — "because / therefore / then"',
            'XI': 'first / then / ordered / items of ranked weight',
            'XX': 'interrogative / ?',
        }

        self.roots = {}
        c_list = list(self.cases.keys())
        t_mul = [3 ** (3 - i) for i in range(4)]
        dig = {0: 'O', 1: 'I', 2: 'X'}  # Is this right?
        for n in range(81):
            rt = self._roots[n]
            root = ['', '', '', '']
            base = n
            for i, c in enumerate(t_mul):
                cd = base // c
                root[i] = dig[cd % 3]
                base -= cd * c
            rt_key = ''.join(root)
            for cn in c_list:
                (ci, co) = cn  #a[:2]
                key = f'{ci}{rt_key[:2]}{co}{rt_key[2:]}'
                if rt == 'CAESURA':
                    value = '–', self._particles[cn]
                else:
                    value = rt, self.cases[cn]
                self.roots[key] = value
        self.rev = {v: k for k, v in self.roots.items()}

    def _expand(self, word: str, case: str, seen: set = None) -> list[tuple]:
        if seen is None:
            seen = set()
        key = word.upper()
        case = case.lower() if case not in self._particles.values() else case
        if key in seen:
            raise ValueError(f"Circular kenning reference: '{key}'")
        add_seen = seen | {key}
        if key not in self.kennings:
            if key == '–':
                return [(word, case)]
            if key == 'CAESURA':
                # Convert case name to particle symbol for the rev lookup
                symbol = self._particles.get(
                    next((c for c, n in self.cases.items() if n == case), case), case
                )
                return [('–', symbol)]
            if key not in self._roots:
                print(f"Unknown word: '{key}'")
            return [(word, case)]

        roots = self.kennings[key]
        result = []
        for i, root in enumerate(roots):
            is_last = (i == len(roots) - 1)
            if isinstance(root, tuple):
                result.extend(self._expand(root[0], root[1], add_seen))
            elif is_last:
                result.extend(self._expand(root, case, add_seen))
            else:
                result.extend(self._expand(root, 'nom', add_seen))
        return result

    def lex(self, script: list[tuple]) -> list[tuple]:
        """
        Lexically expand a script by applying kennings and case rules.
        """
        return [item for group in self.lex_groups(script) for item in group]

    def lex_groups(self, script: list) -> list[list[tuple]]:
        """
        Like lex(), but returns a list of expansion-groups: one inner list per
        input token. A kenning yields a group of multiple ideographs; a plain
        root or punctuation yields a singleton group.
        """
        rev_particles = {v: k for k, v in self._particles.items()}
        groups = []
        for word_case in script:
            if not isinstance(word_case, tuple) and word_case in rev_particles:
                groups.append([('–', word_case)])
            else:
                word, case = word_case if isinstance(word_case, tuple) else (word_case, 'nom')
                groups.append(self._expand(word, case))
        return groups
