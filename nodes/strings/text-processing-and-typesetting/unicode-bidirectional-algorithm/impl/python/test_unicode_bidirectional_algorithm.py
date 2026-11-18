# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-bidirectional-algorithm/. The authors are listed in prov/2X2V4H.jsonl.
# The Bidi_Class values come from unicodedata (unidata_version 16.0.0 with Python 3.14).
# The tests use only characters that are assigned in Unicode 3.2, except the isolate
# controls U+2066 to U+2069, which came in Unicode 6.3.
import random

from unicode_bidirectional_algorithm import MAX_DEPTH, bidi, reorder, visual_order

# The first 40 data lines of BidiCharacterTest-16.0.0.txt (Date: 2024-02-02). Fields:
# code points; paragraph direction (0 LTR, 1 RTL, 2 auto); resolved paragraph level;
# levels, with x for characters removed by X9; visual order.
CONFORMANCE = """\
05D0 05D1 0028 05D2 05D3 005B 0026 0065 0066 005D 002E 0029 0067 0068;0;0;1 1 0 1 1 0 0 0 0 0 0 0 0 0;1 0 2 4 3 5 6 7 8 9 10 11 12 13
05D0 05D1 0028 05D2 05D3 005B 0026 0065 0066 005D 002E 0029 0067 0068;1;1;1 1 1 1 1 1 1 2 2 1 1 1 2 2;12 13 11 10 9 7 8 6 5 4 3 2 1 0
0061 0062 0063 0020 0028 0064 0065 0066 0020 0627 0628 062C 0029 0020 05D0 05D1 05D2;0;0;0 0 0 0 0 0 0 0 0 1 1 1 0 0 1 1 1;0 1 2 3 4 5 6 7 8 11 10 9 12 13 16 15 14
0061 0062 0063 0020 0028 0064 0065 0066 0020 0627 0628 062C 0029 0020 05D0 05D1 05D2;1;1;2 2 2 1 1 2 2 2 1 1 1 1 1 1 1 1 1;16 15 14 13 12 11 10 9 8 5 6 7 4 3 0 1 2
05D0 05D1 05D2 0020 0028 0064 0065 0066 0020 0627 0628 062C 0029 0020 0061 0062 0063;0;0;1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0;2 1 0 3 4 5 6 7 8 11 10 9 12 13 14 15 16
05D0 05D1 05D2 0020 0028 0064 0065 0066 0020 0627 0628 062C 0029 0020 0061 0062 0063;1;1;1 1 1 1 1 2 2 2 1 1 1 1 1 1 2 2 2;14 15 16 13 12 11 10 9 8 5 6 7 4 3 2 1 0
0061 0062 0063 0020 0028 0627 0628 062C 0020 0064 0065 0066 0029 0020 05D0 05D1 05D2;0;0;0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1;0 1 2 3 4 7 6 5 8 9 10 11 12 13 16 15 14
0061 0062 0063 0020 0028 0627 0628 062C 0020 0064 0065 0066 0029 0020 05D0 05D1 05D2;1;1;2 2 2 1 1 1 1 1 1 2 2 2 1 1 1 1 1;16 15 14 13 12 9 10 11 8 7 6 5 4 3 0 1 2
05D0 05D1 05D2 0020 0028 0627 0628 062C 0020 0064 0065 0066 0029 0020 0061 0062 0063;0;0;1 1 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0;2 1 0 3 4 7 6 5 8 9 10 11 12 13 14 15 16
05D0 05D1 05D2 0020 0028 0627 0628 062C 0020 0064 0065 0066 0029 0020 0061 0062 0063;1;1;1 1 1 1 1 1 1 1 1 2 2 2 1 1 2 2 2;14 15 16 13 12 9 10 11 8 7 6 5 4 3 2 1 0
0627 0628 062C 0020 0062 006F 006F 006B 0028 0073 0029;0;0;1 1 1 0 0 0 0 0 0 0 0;2 1 0 3 4 5 6 7 8 9 10
0627 0628 062C 0020 0062 006F 006F 006B 0028 0073 0029;1;1;1 1 1 1 2 2 2 2 2 2 2;4 5 6 7 8 9 10 3 2 1 0
202E 0061 202A 0062 202C 2066 0063 2069 202A 0064 202C 0065 202C;2;0;x 1 x 2 x 1 2 1 x 2 x 1 x;11 9 7 6 5 3 1
202E 0061 202A 0062 202C 2066 0063 2069 202A 0064 202C 0065 202C;1;1;x 3 x 4 x 3 4 3 x 4 x 3 x;11 9 7 6 5 3 1
202D 05D0 202B 05D1 202C 2068 05D2 2069 202B 05D3 202C 05D4 202C;2;1;x 2 x 3 x 2 3 2 x 3 x 2 x;1 3 5 6 7 9 11
202D 0661 202B 0662 202C 2068 0663 2069 202B 0664 202C 0665 202C;0;0;x 2 x 4 x 2 6 2 x 4 x 2 x;1 3 5 6 7 9 11
202A 05D0 0028 05D1 202C 202D 0029;2;1;x 3 3 3 x x 2;3 2 1 6
202A 05D0 0028 05D1 202C 202D 0029 202C;2;1;x 3 3 3 x x 2 x;3 2 1 6
202B 0061 0028 0062 202C 202E 0029;2;0;x 2 2 2 x x 1;6 1 2 3
202B 0061 0028 0062 202C 202E 0029 202C;2;0;x 2 2 2 x x 1 x;6 1 2 3
202A 202E 0061 202C 0028 05D0 202C 202D 0029 202C;2;0;x x 3 x 3 3 x x 2 x;5 4 2 8
202B 202D 05D0 202C 0028 0061 202C 202E 0029 202C;2;1;x x 4 x 4 4 x x 3 x;8 2 4 5
202A 202E 0061 202C 0028 005B 05D0 202C 202D 005D 0029 202C;2;0;x x 3 x 3 3 3 x x 2 2 x;6 5 4 2 9 10
202B 202D 05D0 202C 0028 005B 0061 202C 202E 005D 0029 202C;2;1;x x 4 x 4 4 4 x x 3 3 x;10 9 2 4 5 6
202D 0028 202C 202A 05D0 0029 05D1;2;1;x 2 x x 3 3 3;1 6 5 4
202D 0028 202C 202A 05D0 0029 05D1 202C;2;1;x 2 x x 3 3 3 x;1 6 5 4
202E 0028 202C 202B 0061 0029 0062;2;0;x 1 x x 2 2 2;4 5 6 1
202E 0028 202C 202B 0061 0029 0062 202C;2;0;x 1 x x 2 2 2 x;4 5 6 1
202D 202E 0061 202C 0028 202C 202A 05D0 0029 05D1;2;0;x x 3 x 2 x x 3 3 3;2 4 9 8 7
202E 202D 05D0 202C 0028 202C 202B 0061 0029 0062;2;1;x x 4 x 3 x x 4 4 4;7 8 9 4 2
202D 202E 0061 202C 0028 005B 202C 202A 05D0 005D 0029 05D1;2;0;x x 3 x 2 2 x x 3 3 3 3;2 4 5 11 10 9 8
202E 202D 05D0 202C 0028 005B 202C 202B 0061 005D 0029 0062;2;1;x x 4 x 3 3 x x 4 4 4 4;8 9 10 11 5 4 2
0061 0028 0062 0029 0331;1;1;2 2 2 2 2;0 1 2 3 4
0061 0028 0332 0062 0029 0333;1;1;2 2 2 2 2 2;0 1 2 3 4 5
05D0 0028 05D1 0029 0331;0;0;1 1 1 1 1;4 3 2 1 0
05D0 0028 0332 05D1 0029 0333;0;0;1 1 1 1 1 1;5 4 3 2 1 0
0661 0028 0662 0029 0331;0;0;2 1 2 1 1;4 3 2 1 0
0661 0028 0332 0662 0029 0333;0;0;2 1 1 2 1 1;5 4 3 2 1 0
0041 200F 005B 05D0 005D 200D 20D6;0;0;0 1 1 1 1 x 1;0 6 4 3 2 1
0041 200F 005B 05D0 005D 200D 20D6;1;1;2 1 1 1 1 x 1;6 4 3 2 1 0
"""


def test_conformance_lines():
    lines = CONFORMANCE.splitlines()
    assert len(lines) == 40
    for line in lines:
        cps, d, plevel, levels, order = line.split(";")
        s = "".join(chr(int(h, 16)) for h in cps.split())
        p, lv, vis = bidi(s, None if d == "2" else int(d))
        assert p == int(plevel), line
        assert [("x" if v is None else str(v)) for v in lv] == levels.split(), line
        assert vis == [int(k) for k in order.split()], line


def test_simple_reordering():
    assert reorder("abc") == "abc"
    assert reorder("אבג") == "גבא"
    assert reorder("ab אבג cd") == "ab גבא cd"
    assert reorder("אב 12 גד", 1) == "דג 12 בא"  # numbers keep their order (I2, L2)
    assert bidi("אב")[0] == 1 and bidi("12 ab")[0] == 0 and bidi("12")[0] == 0  # P2, P3
    assert bidi("⁧ab⁩ אב")[0] == 1  # P2 skips the isolate


def test_trailing_whitespace_takes_paragraph_level():
    p, lv, _ = bidi("ab אב  ", 0)
    assert lv == [0, 0, 0, 1, 1, 0, 0]
    p, lv, _ = bidi("אב\tab", 1)  # L1: the segment separator gets the paragraph level
    assert lv == [1, 1, 1, 2, 2]


def test_overflow_of_the_stack():
    s = "‮" * 70 + "a"
    p, lv, _ = bidi(s, 0)
    assert lv[-1] == MAX_DEPTH  # 63 valid overrides reach level 125, the rest overflow
    s = "⁦" * 130 + "a" + "⁩" * 130 + "b"
    p, lv, _ = bidi(s, 0)
    assert max(v for v in lv if v is not None) <= MAX_DEPTH + 1
    assert lv[-1] == 0


def test_bracket_pairs_and_the_stack_of_bd16():
    # N0: the pair holds only R and R comes before it, so the brackets become R.
    assert bidi("א(ב)a", 0)[1] == [1, 1, 1, 1, 0]
    # Without N0, N1 would give the closing bracket the embedding direction L.
    for k, closing in ((63, 1), (64, 0)):
        s = "א" + "(" * k + "ב" + ")" * k + "a"
        lv = bidi(s, 0)[1]
        assert lv[k + 2] == closing  # at 64 openers BD16 returns no pairs at all
    # U+2329 and U+3009 form a pair, because U+2329 decomposes to U+3008.
    assert bidi("א〈ב〉a", 0)[1] == [1, 1, 1, 1, 0]
    assert bidi("א〈ב〉a", 0)[1] == [1, 1, 1, 1, 0]


def _reference_levels(s, p):
    """A direct reading of W2, W7, N1, N2, I1, I2 and L1 for text with no explicit
    formatting, no brackets and no marks: one isolating run sequence at level p."""
    import unicodedata
    t = [unicodedata.bidirectional(c) for c in s]
    e = "R" if p else "L"
    x, last = [], e
    for c in t:
        if c in ("L", "R", "AL"):
            last = c
        x.append("AN" if c == "EN" and last == "AL" else c)
    x = ["R" if v == "AL" else v for v in x]
    last = e
    for k, v in enumerate(x):
        if v in ("L", "R"):
            last = v
        elif v == "EN" and last == "L":
            x[k] = "L"
    def strong(v):
        return "L" if v == "L" else "R" if v in ("R", "EN", "AN") else None
    out = list(x)
    for k, v in enumerate(x):
        if v == "WS":
            left = next((strong(x[j]) for j in range(k - 1, -1, -1) if strong(x[j])), e)
            right = next((strong(x[j]) for j in range(k + 1, len(x)) if strong(x[j])), e)
            out[k] = left if left == right else e
    lv = []
    for v in out:
        if p == 0:
            lv.append({"L": 0, "R": 1, "EN": 2, "AN": 2}[v])
        else:
            lv.append({"L": 2, "R": 1, "EN": 2, "AN": 2}[v])
    k = len(s) - 1
    while k >= 0 and t[k] == "WS":
        lv[k] = p
        k -= 1
    return lv


def test_against_reference_on_simple_text():
    rng = random.Random(9)
    alphabet = "ab אב" + "ابت" + "12" + "١٢"
    for _ in range(600):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 10)))
        for p in (0, 1):
            assert bidi(s, p)[1] == _reference_levels(s, p), (s, p)


def _tree_order(levels, idx, v, low):
    """L2 by recursion on a block whose characters all have level v or more: the
    characters at level v stay, and each maximal sub-block above v is ordered as a block
    of level v + 1. L2 reverses the block once for v itself if v >= low, the lowest odd
    level of the line."""
    out, k = [], 0
    while k < len(idx):
        if levels[idx[k]] == v:
            out.append(idx[k])
            k += 1
        else:
            j = k
            while j < len(idx) and levels[idx[j]] > v:
                j += 1
            out.extend(_tree_order(levels, idx[k:j], v + 1, low))
            k = j
    return out[::-1] if v >= low else out


def test_l2_against_recursive_definition():
    rng = random.Random(51)
    for _ in range(800):
        n = rng.randint(0, 12)
        levels = [rng.choice([0, 1, 2, 3, 4, None]) for _ in range(n)]
        kept = [i for i in range(n) if levels[i] is not None]
        low = min((levels[i] for i in kept if levels[i] % 2 == 1), default=99)
        assert visual_order(levels) == _tree_order(levels, kept, 0, low), levels


def test_order_is_a_permutation_of_the_kept_characters():
    rng = random.Random(3)
    alphabet = "ab אב12١(),.‪‫‬‭‮⁦⁧⁨⁩‎‏́"
    for _ in range(400):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
        for d in (0, 1, None):
            p, lv, order = bidi(s, d)
            assert sorted(order) == [i for i, v in enumerate(lv) if v is not None]
            assert all(v is None or p <= v <= MAX_DEPTH + 1 for v in lv)
