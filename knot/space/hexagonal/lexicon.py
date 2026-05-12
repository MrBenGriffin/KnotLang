# from ..cell import Cell
# from dim import Dim

class Lexicon:
    def __init__(self):
        # ALL internal elements — fixed case as specified or NOM
        # terminal element — ALWAYS takes live case, never fixed
        self.kennings = {
            # These are non-kenning composites - used to match swadesh etc.
            # differentiated by having a fixed case terminal.
            'WORKED': [('WORK', 'int')],  # VERB[intrans] + NOUN = the verb-ed noun= result state encoded in compound
            'BURN': [('FIRE', 'int')],
            'HEAR': [('EAR', 'int')],
            'SMELL': [('NOSE', 'int')],
            'SEE': [('EYE', 'int')],
            'TASTE': [('MOUTH', 'int')],
            # 'FAST': [('SOON', 'int')],
            # 'SLOW': [('LONG', 'int')],
            'WHO': [('SELF', 'nom'), ('CAESURA', '?')],
            'WHAT': [('SELF', 'abs'), ('CAESURA', '?')],
            'WHERE': [('SELF', 'loc'), ('CAESURA', '?')],
            'WHEN': ['WHERE', 'TIME', ('CAESURA', '?')],
            # HOW = PATH[abs]·?
            # 'Why' is disambiguated...
            # - Causal — what caused this? = PATH[abs]·? looking backward
            # - Consequential — to what end? = POINT[abs]·? looking forward
            # - Motivational — from what feeling/desire? = HEART[abs]·? looking inward
            # - Logical — by what reasoning? = KNOW[abs]·? looking at the structure

            # There are kennings proper. no nom. suffix.
            'PET': ['HOUSE', 'ANIMAL'],
            'DOG': ['WATCH', 'PET'],
            'CAT': ['HUNT', 'PET'],
            'KITTEN': ['CAT', 'CHILD'],
            'PUPPY': ['DOG', 'CHILD'],
            'TINY': ['SMALL', 'SMALL'],
            'SIZE': ['SMALL', 'LARGE'],
            'COUNT': ['ONE', 'MANY'],
            'BIG': ['LARGE'],
            'HUGE': ['LARGE', 'LARGE'],
            'FLY': ['WIND', 'MOVE'],
            'SWIM': ['WATER', 'MOVE'],
            'SEED': ['MAYBE', 'CHILD'],
            'FISH': ['WATER', 'ANIMAL'],
            'BIRD': ['WIND', 'ANIMAL'],
            'BLOOD': ['HEART', 'WATER'],
            'INSECT': ['EARTH', 'ANIMAL'],
            'TREE': ['WOOD', 'PLANT'],
            'LEAF': ['LIGHT', 'REAP', 'PLANT', 'EDGE'],
            'SHARP': ['POINT'],
            'BARK': ['TREE', 'SKIN'],
            'SKIN': ['BODY', 'EDGE'],
            'SOFT': [('NOT', 'adj'), 'POINT'],
            'SMOOTH': ['LEVEL', 'ALIKE', 'FEEL'],
            'HARD': ['METAL', 'ALIKE', 'FEEL'],
            'TEXTURE': ['SHARP', 'SOFT'],
            'FUR': ['SOFT', 'SKIN'],
            'GRASS': ['HAIR', 'PLANT'],
            'FLUID': ['WATER', 'ALIKE', 'FEEL'],
            'SOLID': ['GROUND', 'ALIKE', 'FEEL'],
            'FOREST': ['TREE', 'TREE'],
            'LEATHER': ['HUNT', 'SKIN'],
            'CLOTHING': ['WEAVE', 'SKIN'],
            'NEW': ['NOT', 'PRIOR'],  # (fresh, novel)
            'WAS': ['TIME', 'PRIOR'],
            'WILL': ['TIME', 'NEXT'],
            'KNOT': ['WEAVE', 'STRING'],
            'CLOUD': ['SKY', 'KNOT'],
            'SMOKE': ['FIRE', 'KNOT'],
            'ASH': ['FIRE', 'REAP'],
            'MAZE': ['PATH', 'KNOT'],
            'FACT': ['KNOW', 'GROUND'],
            'SURE': ['KNOW', 'KNOW'],
            'TRUTH': ['KNOW', 'FACT'],
            'BELIEF': ['HOLD', 'FACT'],
            'FLESH': ['HUNT', 'FOOD'],
            'FEATHER': ['BIRD', 'EDGE'],
            'GREASE': ['BODY', 'FIRE', 'WATER'],
            'LOUSE': ['SMALL', 'BLOOD', 'REAP'],
            'EGG': ['SEED', 'BONE'],
            'HORN': ['POINT', 'BONE'],
            'TAIL': ['BONE', 'EDGE'],
            'CLAW': ['HAND', 'EDGE', 'BONE'],
            'HAIR': ['SOFT', 'SKIN'],
            'FACE': ['EYE', 'NOSE', 'CIRCLE'],
            'HEAD': ['EYE', 'NOSE', 'GROUND'],
            'FOOT': ['GROUND', 'HAND'],
            'LEG': ['MOVE', 'BODY'],
            'KNEE': ['LEG', 'BONE'],
            'ARM': ['HAND', 'BODY'],
            'ELBOW': ['ARM', 'BONE'],
            'FINGERNAIL': ['CLAW'],
            'BELLY': ['HERE', 'BODY'],
            'STOMACH': ['FOOD', 'BODY'],
            'NECK': ['VOICE', 'BODY'],
            'CHEST': ['BREATH', 'BODY'],
            'BREAST': ['MOTHER', 'BODY'],
            'BREASTS': ['BOTH', 'BREAST'],
            'LIVER': ['BLOOD', 'FLESH'],
            'TOOTH': ['MOUTH', 'BONE'],
            'TONGUE': ['HIDE', 'MOUTH'],
            'BITE': ['BREAK', 'TOOTH'],  # verb.
            'BITE.n': ['TOOTH', 'BREAK'], # noun.
            'FRUIT': ['SEED', 'HOLD'],
            'ENJOY': ['MOVE', 'HEART'],
            'KNOWLEDGE': ['HOLD', 'KNOW'],
            # geology
            'STONE': ['GROUND', 'ROOT'],
            'ROCK': ['STONE'],
            'SAND': ['WIND', 'EARTH'],
            'MOUNTAIN': ['POINT', 'GROUND'],
            'ORE': ['REAP', 'METAL'],
            'MINE': ['METAL', 'REAP'],
            'RIVER': ['WATER', 'PATH'],
            'GOLD': ['HEART', 'METAL'],
            'SILVER': ['MIRROR', 'METAL'],
            # ...
            'GRIEF': ['METAL', 'HEART'],
            'PICTURE': ['VOICE', 'EYE'],
            'DRAW': ['PICTURE', 'HAND'],
            'LANGUAGE': ['VOICE', 'HARNESS'],
            'MIRROR': ['WATER', 'SELF'],
            'ECHO': ['MIRROR', 'VOICE'],
            'WRITE': ['VOICE', 'HAND'],
            'PRIMORDIAL': ['PRIOR', 'PRIOR'],
            'ORIGIN': ['ROOT', 'STRING'],
            'SOURCE': ['STRING', 'ROOT'],
            'STORY': ['VOICE', 'WEAVE'],
            'HISTORY': ['TIME', 'WEAVE'],
            'FALSEHOOD': ['NOT', 'FACT', 'VOICE'],
            'SAY': ['VOICE'],
            'TRADITIONAL': [('STRING', 'gen')],
            'ANCESTOR': ['PRIOR', 'PERSON'],
            'MYTH': ['SOURCE', 'STORY'],
            'EPIC': ['TRADITIONAL', 'STORY'],
            'LEGEND': ['ANCESTOR', 'STORY'],
            'GOD': ['SKY', 'MOTHER', 'ONE'],
            'KING': ['POINT', 'MAN'],
            'QUEEN': ['POINT', 'WOMAN'],
            'PRINCE': ['KING', 'CHILD'],
            'PEACE': ['HEART', 'MEND'],
            'SUN': ['DAY', 'LIGHT', 'GIVE'],
            'MOON': ['NIGHT', 'LIGHT', 'GIVE'],
            'STAR': ['NIGHT', 'LIGHT', 'POINT'],
            'PRECIPITATE': ['SKY', 'FALL'],
            'RAIN': ['FALL', 'WATER'],
            'BEING': ['BREATH', 'ONE'],
            'PERSON': [('NAME', 'agt'), 'ONE'],
            'PEOPLE': ['MANY', 'PERSON'],
            # measures
            'DISTANT': ['LARGE', 'BETWEEN'],
            'SHORT': ['SMALL', 'BETWEEN'],
            'NEAR': ['SHORT', 'SPACE'],
            'GAP': ['BETWEEN', 'SPACE'],
            'FAR': ['DISTANT', 'SPACE'],
             # 'LONG': ['DISTANT', 'SPACE'], # Use FAR
            'SOON': ['SHORT', 'TIME'],    # SOON.intr quick
            'LONG': ['DISTANT', 'TIME'],  # TIME
            'INTERVAL': ['BETWEEN', 'TIME'],
            'DISC': [('FIELD', 'adj'), 'CIRCLE'],
            'ROUND': ['CIRCLE', 'PATH'],
            'FULL': ['DISC'],
            'ENTIRE': ['DISC'],

            'AGAIN': ['PRIOR', 'ALIKE'],
            'EXCHANGE': ['BETWEEN', 'GIVE'],
            'ALL': [('FIELD', 'abs'), 'CIRCLE'],
            'ALWAYS': [('DISC', 'adj'), 'TIME'],
            'EVERYWHERE': [('DISC', 'adj'), 'SPACE'],
            'DRINK.n': ['WATER', 'FOOD'],
            'DRINK': ['WATER', 'EAT'],
            # hot/cold
            'HOT': ['FIRE', 'FEEL'],
            'COLD': ['WATER', 'FEEL'],
            'DRY': ['HIDE', 'WATER'],
            'WET': ['HOLD', 'WATER'],
            # colours - anything can be used to give colour but for swadesh..
            'WHITE': ['LIGHT', 'COLOUR'],
            'BLACK': ['NIGHT', 'COLOUR'],
            'RED': ['HEART', 'COLOUR'],
            'YELLOW': ['FIRE', 'COLOUR'],
            'GREEN': ['PLANT', 'COLOUR'],
            'BLUE': ['SKY', 'COLOUR'],
            'BROWN': ['EARTH', 'COLOUR'],
            'SHADOW': ['NIGHT', 'ALIKE'],
            'GREY': ['SHADOW', 'COLOUR'],
            # ethics
            'HARM': ['FEAR', 'GIVE'],
            'BAD': ['HARM'],
            'GOOD': [('GIVE', 'agt'), 'NOT', 'FEAR'],
            'EVIL': [('HARM', 'agt'), 'REAP'],
            'LIFE': ['BREATH'],
            'DEATH': ['NOT', 'BREATH'],
            'DIE': ['BREAK', 'BREATH'],
            'KILL': [('BREAK', 'trn'), 'BREATH'],
            # Pronouns
            'I': [('SELF', 'int'), 'SELF'],
            'WE': ['MANY', 'I'],
            'YOU': [('NOT', 'acc'), 'SELF'],
            'YALL': ['MANY', 'YOU'],
            'IT': [('NOT', 'abs'), 'SELF'],
            'S/HE': ['NOT', 'SELF'],  # ungendered, singular 'they'
            'HE': ['MAN', 'S/HE'],
            'SHE': ['WOMAN', 'S/HE'],
            'THEY': ['MANY', 'S/HE'],  # they, animate
            'THEY_': ['MANY', 'IT'],  # they non-animate (multiple its)
            'THERE': [('NOT', 'abs'), 'HERE'],
            'THAT': ['THERE', 'SELF'],
            'THIS': ['HERE', 'SELF'],
            'THOSE': ['MANY', 'THAT'],
            'THESE': ['MANY', 'THIS'],
            'COME': [('HERE', 'loc'), 'MOVE'],
            'GO': [('THERE', 'loc'), 'MOVE'],
            'RETURN': ['AGAIN', 'COME'],
            'WALK': ['FOOT', 'MOVE'],
            'LIE': ['LEVEL', 'BODY'],
            'SIT': ['GROUND', 'BODY'],
            'STAND': ['MOVE', 'BODY'],
            'SEAT': ['SIT', 'HOLD'],
            'BET': ['LIE', 'HOLD'],

            'HER': [('NOT', 'gen'), 'SELF'],  # ungendered, same
            # THIS/THAT/WHO/WHAT
            # kinship
            'MUM': ['WOMAN', 'MOTHER'],
            'FATHER': ['MAN', 'MOTHER'],

            # numeric words
            # ACC = subtraction(-). NOM = addition(+), GEN = multiplication(×), AGT = exponentiation(^)
            # BREAK = half, ONE = 1, NEXT = 2, CIRCLE = 6
            'TWO': ['NEXT'],
            'BOTH': ['ONE', 'ONE'],
            'THREE': [('BREAK', 'gen'), 'CIRCLE'],
            'FOUR': [('NEXT', 'acc'), 'CIRCLE'],
            'FIVE': [('ONE', 'acc'), 'CIRCLE'],
            'SIX': ['CIRCLE'],
            'SEVEN': ['CIRCLE', 'ONE'],
            'EIGHT': ['CIRCLE', 'NEXT'],
            'NINE': ['CIRCLE', 'THREE'],
            'TEN': [('NEXT', 'acc'), 'TWELVE'],
            'ELEVEN': [('ONE', 'acc'), 'TWELVE'],
            'TWELVE': [('NEXT', 'gen'), 'CIRCLE'],
            'NUMERIC_MODE': [('POSITION', 'gen'), ('ONE', 'abs')]
        }
        # AND=>STRING
        # MAYBE=>BALANCE ?
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
        if key in seen:
            raise ValueError(f"Circular kenning reference: '{key}'")
        add_seen = seen | {key}  #
        if key not in self.kennings:
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
        rev_particles = {v: k for k, v in self._particles.items()}
        result = []
        for word_case in script:
            if not isinstance(word_case, tuple) and word_case in rev_particles:
                result.append(('–', word_case))
            else:
                word, case = word_case if isinstance(word_case, tuple) else (word_case, 'nom')
                result.extend(self._expand(word, case))
        return result
