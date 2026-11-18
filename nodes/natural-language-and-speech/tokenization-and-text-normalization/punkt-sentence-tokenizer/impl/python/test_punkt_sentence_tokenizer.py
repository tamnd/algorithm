# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/punkt-sentence-tokenizer/. The authors are listed in prov/BAJBZ1.jsonl.

import math
import random

from punkt_sentence_tokenizer import (
    NUMBER, abbreviation_log_lambda, abbreviation_score, dunning_log_lambda, punkt, split_sentences,
    tokenize,
)

# A block of lines; three of them hold two sentences. The page example repeats it 5 times.
BLOCK = [
    "The dog met Dr. Brown at the park.", "We saw Dr. Brown and the cat.",
    "They sold apples, pears etc. and the rest.", "She came home late.",
    "However, the dog ran to the park.", "J. Smith saw the cat.", "The cat saw J. Smith at home.",
    "We bought pears etc. Then we went home.", "On 12. May the shop was closed.", "The park was quiet.",
    "We ate and then we slept.", "However, it rained.", "However, we stayed home.",
    "We sold pears etc. However, the cat slept.", "Mo. Brown left.",
]
TRUE_SENTENCES = []
for line in BLOCK:
    if line == "We bought pears etc. Then we went home.":
        TRUE_SENTENCES += ["We bought pears etc.", "Then we went home."]
    elif line == "We sold pears etc. However, the cat slept.":
        TRUE_SENTENCES += ["We sold pears etc.", "However, the cat slept."]
    else:
        TRUE_SENTENCES.append(line)


def test_table2_of_the_paper():
    # Kiss and Strunk (2006), Table 2: N = 351,529 WSJ tokens. C(.) is not given in the paper;
    # 20,994 periods (p = 0.0597) reproduce the printed values.
    n, c_period = 351529, 20994
    rows = [  # type, C(w, .), C(w, not .), revised log lambda, scaled log lambda
        ("n.h", 5, 0, 28.08, 7.60), ("u.s.a", 5, 0, 28.08, 4.19), ("alex", 8, 2, 26.75, 0.03),
        ("ounces", 4, 0, 22.46, 0.06), ("a.g", 4, 0, 22.46, 6.08), ("ga", 4, 0, 22.46, 3.04),
        ("vt", 4, 0, 22.46, 3.04), ("ore", 5, 1, 18.99, 0.32), ("mo", 8, 3, 17.67, 0.30),
        ("m.j", 3, 0, 16.85, 4.56), ("depositor", 3, 0, 16.85, 0.00), ("reps", 3, 0, 16.85, 0.31),
        ("u.n", 3, 0, 16.85, 4.56),
    ]
    for w, k, m, ll, scaled in rows:
        assert round(abbreviation_log_lambda(k, m, c_period, n), 2) == ll
        assert round(abbreviation_score(w, k, m, c_period, n), 2) == scaled
    # The table prints 0.26 for 1990s (5, 1); the formula of the paper gives 18.99 e^-5 / 5 = 0.03.
    assert round(abbreviation_score("1990s", 5, 1, c_period, n), 2) == 0.03
    # mo is printed as 0.30, but its unrounded score is just below the threshold 0.3.
    assert 0.298 < abbreviation_score("mo", 8, 3, c_period, n) < 0.3


def test_table1_of_the_paper():
    # Frequent sentence starters in German: C(<S>) = 35,775, N = 847,206.
    n, cs = 847206, 35775
    rows = [("ist", 9758, 182, 169.8390), ("zu", 7643, 71, 298.8915),
            ("dennoch", 231, 80, 221.4709), ("erstens", 38, 21, 82.1377)]
    for w, c2, c12, ll in rows:
        assert abs(dunning_log_lambda(cs, c2, c12, n) - ll) < 0.002
    # The one-sided test keeps dennoch and erstens and drops ist and zu.
    assert [c12 * n > c2 * cs for _, c2, c12, _ in rows] == [False, False, True, True]


def test_tokenize():
    toks = tokenize('He said "end.)" at 12. U.S. wait... Why? Dr. x')
    assert [(t.kind, t.word, t.type) for t in toks] == [
        ("", "He", "he"), ("", "said", "said"), (".", "end", "end"), ("", "at", "at"),
        (".", "12", NUMBER), (".", "U.S", "u.s"), ("...", "wait", "wait"), ("?", "Why", "why"),
        (".", "Dr", "dr"), ("", "x", "x"),
    ]
    assert toks[2].start == 8 and toks[2].end == 15


def test_page_example():
    text = " ".join(BLOCK * 5)
    toks, ends, model = punkt(text)
    assert len(toks) == 445 and sum(t.kind == "." for t in toks) == 120
    assert model.abbrevs == {"dr", "etc", "j", "mo"}
    assert model.starters == {"however", "we"}
    assert split_sentences(text) == TRUE_SENTENCES * 5
    # Without the token stage, three periods in each block are wrong.
    first = [t.kind == "?" or (t.kind == "." and t.type not in model.abbrevs) for t in toks]
    first[-1] = True
    assert sum(a != b for a, b in zip(first, ends)) == 3 * 5


def test_small_text_pitfall():
    # Words that always end a sentence look like abbreviations when the text is small and repetitive.
    _, _, model = punkt(" ".join(BLOCK * 8))
    assert {"late", "left", "rest"} <= model.abbrevs


def test_edge_cases():
    assert punkt("")[1] == [] and split_sentences("") == []
    assert split_sentences("no period here") == ["no period here"]
    assert split_sentences("Why? Because.") == ["Why?", "Because."]
    assert split_sentences("  Hello.  ") == ["Hello."]


# ---------------------------------------------------------------------------
# A slow oracle that counts by scanning the token list for every question.

def _logpmf(k, n, x):
    if (k > 0 and x <= 0.0) or (n - k > 0 and x >= 1.0):
        return -math.inf
    out = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    if k > 0:
        out += k * math.log(x)
    if n - k > 0:
        out += (n - k) * math.log(1.0 - x)
    return out


def _dunning(c1, c2, c12, n):
    p, p1 = c2 / n, c12 / c1
    p2 = (c2 - c12) / (n - c1) if n > c1 else 0.0
    return 2.0 * (_logpmf(c12, c1, p1) + _logpmf(c2 - c12, n - c1, p2)
                  - _logpmf(c12, c1, p) - _logpmf(c2 - c12, n - c1, p))


def oracle_ends(text):
    toks = tokenize(text)
    n = len(toks)
    if n == 0:
        return []
    memo = {}

    def count(w):
        if ("c", w) not in memo:
            memo[("c", w)] = sum(t.type == w for t in toks)
        return memo[("c", w)]

    c_dot = sum(t.kind == "." for t in toks)

    def abbrev(w):
        key = ("a", w)
        if key not in memo:
            k = sum(t.type == w and t.kind == "." for t in toks)
            ok = False
            if k > 0 and w != NUMBER and any(ch.isalpha() for ch in w):
                m = count(w) - k
                ll = -2.0 * (_logpmf(k, k + m, c_dot / n) - _logpmf(k, k + m, 0.99))
                length = len(w) - w.count(".")
                ok = ll * math.exp(-length) * (w.count(".") + 1) / length ** m >= 0.3
            memo[key] = ok
        return memo[key]

    def initial(t):
        return t.kind == "." and len(t.type) == 1 and t.type.isalpha()

    def number(t):
        return t.kind == "." and t.type == NUMBER

    first = [t.kind == "?" or (t.kind == "." and not abbrev(t.type)) for t in toks]

    def position(i):
        if i == 0:
            return "start"
        p = toks[i - 1]
        if p.kind == "..." or (p.kind == "." and (not first[i - 1] or initial(p) or number(p))):
            return None
        return "start" if first[i - 1] else "mid"

    def seen(w, upper, where):
        for i, t in enumerate(toks):
            if t.type != w:
                continue
            c = t.word[:1]
            if (c.isupper() if upper else c.islower()) and position(i) in where:
                return True
        return False

    def ortho(u):
        if all(ch in ";:,.!?" for ch in u.word):
            return False
        w, c = u.type, u.word[:1]
        if c.isupper() and seen(w, False, ("start", "mid")) and not seen(w, True, ("mid",)):
            return True
        if c.islower() and (seen(w, True, ("start", "mid")) or not seen(w, False, ("start",))):
            return False
        return None

    sure = [i for i in range(n - 1)
            if toks[i].kind == "." and first[i] and not initial(toks[i]) and not number(toks[i])]

    def starter(w):
        c12 = sum(toks[i + 1].type == w for i in sure)
        return c12 > 0 and _dunning(len(sure), count(w), c12, n) >= 30 and c12 * n > count(w) * len(sure)

    def colloc(t, u):
        c12 = sum(toks[j].kind == "." and toks[j].type == t.type and toks[j + 1].type == u.type
                  for j in range(n - 1))
        c1 = count(t.type)
        return c12 > 0 and _dunning(c1, count(u.type), c12, n) >= 7.88 and c12 * n > count(u.type) * c1

    ends = list(first)
    for i in range(n - 1):
        t, u = toks[i], toks[i + 1]
        if t.kind == "..." or (t.kind == "." and abbrev(t.type) and not initial(t)):
            ends[i] = ortho(u) is True or (u.word[:1].isupper() and starter(u.type))
        elif initial(t) or number(t):
            o = ortho(u)
            if (colloc(t, u) and not starter(u.type)) or o is False:
                ends[i] = False
            elif initial(t) and o is None and u.word[:1].isupper() and not seen(u.type, False, ("start", "mid")):
                ends[i] = False
    ends[-1] = True
    return ends


WORDS = ["The", "the", "Dr.", "dr.", "etc.", "Then", "then", "However,", "J.", "Smith", "12.", "7",
         "May", "may", "wait...", "Why?", "No!", "cat", "cat.", "dog.", "Brown", "park.", "U.S.", "a", "A",
         "and", "we", "We", ",", '"Hi."', "(end.)", "--", "x."]


def test_random_against_oracle():
    rng = random.Random(2006)
    for case in range(500):
        if case % 2 == 0:
            text = " ".join(rng.choice(WORDS) for _ in range(rng.randint(0, 60)))
        else:
            text = " ".join(rng.choice(BLOCK) for _ in range(rng.randint(1, 45)))
        toks, ends, model = punkt(text)
        assert ends == oracle_ends(text)
        if toks:
            assert ends[-1]
        for t, e in zip(toks[:-1], ends[:-1]):
            if t.kind == "?":
                assert e
            elif t.kind == "":
                assert not e
            elif t.kind == "." and t.type not in model.abbrevs and t.type != NUMBER and len(t.type) != 1:
                assert e  # an ordinary word with a period always ends a sentence
        assert "".join(split_sentences(text)).replace(" ", "") == text.replace(" ", "")
