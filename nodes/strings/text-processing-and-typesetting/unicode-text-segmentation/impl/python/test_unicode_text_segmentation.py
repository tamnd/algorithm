# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-text-segmentation/. The authors are listed in prov/DB4AFE.jsonl.

import random
import re

from unicode_text_segmentation import (
    ext_pict,
    gcb,
    grapheme_boundaries,
    grapheme_clusters,
    incb,
    sentence_boundaries,
    word_boundaries,
)

# Lines copied from GraphemeBreakTest-16.0.0.txt (Date: 2024-05-02, 15:02:48 GMT),
# https://www.unicode.org/Public/16.0.0/ucd/auxiliary/GraphemeBreakTest.txt.
# Only the part before the tab and "#" is copied. The first group is file lines 24 to 61
# (consecutive data lines). The second group is from the hand-written lines at the end of the file.
GRAPHEME_LINES = """\
÷ 0020 ÷ 0020 ÷
÷ 0020 × 0308 ÷ 0020 ÷
÷ 0020 ÷ 000D ÷
÷ 0020 × 0308 ÷ 000D ÷
÷ 0020 ÷ 000A ÷
÷ 0020 × 0308 ÷ 000A ÷
÷ 0020 ÷ 0001 ÷
÷ 0020 × 0308 ÷ 0001 ÷
÷ 0020 × 200C ÷
÷ 0020 × 0308 × 200C ÷
÷ 0020 ÷ 1F1E6 ÷
÷ 0020 × 0308 ÷ 1F1E6 ÷
÷ 0020 ÷ 0600 ÷
÷ 0020 × 0308 ÷ 0600 ÷
÷ 0020 × 0A03 ÷
÷ 0020 × 0308 × 0A03 ÷
÷ 0020 ÷ 1100 ÷
÷ 0020 × 0308 ÷ 1100 ÷
÷ 0020 ÷ 1160 ÷
÷ 0020 × 0308 ÷ 1160 ÷
÷ 0020 ÷ 11A8 ÷
÷ 0020 × 0308 ÷ 11A8 ÷
÷ 0020 ÷ AC00 ÷
÷ 0020 × 0308 ÷ AC00 ÷
÷ 0020 ÷ AC01 ÷
÷ 0020 × 0308 ÷ AC01 ÷
÷ 0020 × 0903 ÷
÷ 0020 × 0308 × 0903 ÷
÷ 0020 ÷ 0904 ÷
÷ 0020 × 0308 ÷ 0904 ÷
÷ 0020 ÷ 0D4E ÷
÷ 0020 × 0308 ÷ 0D4E ÷
÷ 0020 ÷ 0915 ÷
÷ 0020 × 0308 ÷ 0915 ÷
÷ 0020 ÷ 231A ÷
÷ 0020 × 0308 ÷ 231A ÷
÷ 0020 × 0300 ÷
÷ 0020 × 0308 × 0300 ÷
÷ 000D × 000A ÷ 0061 ÷ 000A ÷ 0308 ÷
÷ 0061 × 0308 ÷
÷ 0020 × 200D ÷ 0646 ÷
÷ 0646 × 200D ÷ 0020 ÷
÷ 1100 × 1100 ÷
÷ AC00 × 11A8 ÷ 1100 ÷
÷ AC01 × 11A8 ÷ 1100 ÷
÷ 1F1E6 × 1F1E7 ÷ 1F1E8 ÷ 0062 ÷
÷ 0061 ÷ 1F1E6 × 1F1E7 ÷ 1F1E8 ÷ 0062 ÷
÷ 0061 ÷ 1F1E6 × 1F1E7 × 200D ÷ 1F1E8 ÷ 0062 ÷
÷ 0061 ÷ 1F1E6 × 200D ÷ 1F1E7 × 1F1E8 ÷ 0062 ÷
÷ 0061 ÷ 1F1E6 × 1F1E7 ÷ 1F1E8 × 1F1E9 ÷ 0062 ÷
÷ 0061 × 200D ÷
÷ 0061 × 0308 ÷ 0062 ÷
÷ 0061 × 0903 ÷ 0062 ÷
÷ 0061 ÷ 0600 × 0062 ÷
÷ 1F476 × 1F3FF ÷ 1F476 ÷
÷ 0061 × 1F3FF ÷ 1F476 ÷
÷ 0061 × 1F3FF ÷ 1F476 × 200D × 1F6D1 ÷
÷ 1F476 × 1F3FF × 0308 × 200D × 1F476 × 1F3FF ÷
÷ 1F6D1 × 200D × 1F6D1 ÷
÷ 0061 × 200D ÷ 1F6D1 ÷
÷ 2701 × 200D × 2701 ÷
÷ 0061 × 200D ÷ 2701 ÷
÷ 0915 ÷ 0924 ÷
÷ 0915 × 094D × 0924 ÷
÷ 0915 × 094D × 094D × 0924 ÷
÷ 0915 × 094D × 200D × 0924 ÷
÷ 0915 × 093C × 200D × 094D × 0924 ÷
÷ 0915 × 093C × 094D × 200D × 0924 ÷
÷ 0915 × 094D × 0924 × 094D × 092F ÷
÷ 0915 × 094D ÷ 0061 ÷
÷ 0061 × 094D ÷ 0924 ÷
÷ 003F × 094D ÷ 0924 ÷
÷ 0378 × 094D ÷
÷ 0378 × 200D ÷
÷ 0378 ÷ 0378 ÷
"""

# Lines copied from WordBreakTest-16.0.0.txt (Date: 2024-04-30, 21:48:43 GMT), from the
# hand-written lines and the last block of the file.
WORD_LINES = """\
÷ 0031 ÷ 002C × 200D ÷
÷ 0031 × 002C × 0308 × 0031 ÷ 0027 ÷
÷ 0031 × 002E × 2060 × 0031 ÷ 0027 ÷
÷ 0031 ÷ 002E × 2060 ÷ 05D0 ÷
÷ 0020 × 200D ÷ 0646 ÷
÷ 0646 × 200D ÷ 0020 ÷
÷ 05D0 × 0027 ÷
÷ 05D0 × 0022 × 05D0 ÷
÷ 3031 × 3031 ÷
÷ 0041 × 005F × 0030 × 005F × 3031 × 005F ÷
÷ 1F1E6 × 1F1E7 ÷ 1F1E8 ÷ 0062 ÷
÷ 0061 ÷ 1F1E6 × 1F1E7 × 200D ÷ 1F1E8 ÷ 0062 ÷
÷ 0061 ÷ 1F1E6 × 200D × 1F1E7 ÷ 1F1E8 ÷ 0062 ÷
÷ 0061 ÷ 1F1E6 × 1F1E7 ÷ 1F1E8 × 1F1E9 ÷ 0062 ÷
÷ 1F6D1 × 200D × 1F6D1 ÷
÷ 0061 × 200D × 1F6D1 ÷
÷ 2701 × 200D × 2701 ÷
÷ 0061 × 200D × 2701 ÷
÷ 1F476 × 1F3FF × 0308 × 200D × 1F476 × 1F3FF ÷
÷ 200D × 1F6D1 × 1F3FF ÷
÷ 200D × 1F6D1 ÷
÷ 0061 × 0308 × 200D × 0308 × 0062 ÷
÷ 0061 ÷ 0020 × 0020 ÷ 0062 ÷
÷ 0061 ÷ 003A ÷ 003A ÷ 0031 ÷
÷ 0031 ÷ 002C ÷ 003A ÷ 0031 ÷
÷ 0031 × 005F × 0061 ÷ 002E ÷ 002C ÷ 0031 ÷
÷ 0061 × 005F × 0061 ÷ 002C ÷ 002C ÷ 0061 ÷
"""

# Lines copied from SentenceBreakTest-16.0.0.txt (16.0.0), from the hand-written lines.
SENTENCE_LINES = """\
÷ 0061 × 0308 ÷
÷ 0020 × 200D × 0646 ÷
÷ 0646 × 200D × 0020 ÷
÷ 0028 × 0022 × 0047 × 006F × 002E × 0022 × 0029 × 0020 ÷ 0028 × 0048 × 0065 × 0020 × 0064 × 0069 × 0064 × 002E × 0029 ÷
÷ 0028 × 201C × 0047 × 006F × 003F × 201D × 0029 × 0020 ÷ 0028 × 0048 × 0065 × 0020 × 0064 × 0069 × 0064 × 002E × 0029 ÷
÷ 0055 × 002E × 0053 × 002E × 0041 × 0300 × 002E × 0020 × 0069 × 0073 ÷
÷ 0055 × 002E × 0053 × 002E × 0041 × 0300 × 003F × 0020 ÷ 0048 × 0065 ÷
÷ 0055 × 002E × 0053 × 002E × 0041 × 0300 × 002E ÷
÷ 0033 × 002E × 0034 ÷
÷ 0063 × 002E × 0064 ÷
÷ 0043 × 002E × 0064 ÷
÷ 0063 × 002E × 0044 ÷
÷ 0043 × 002E × 0044 ÷
÷ 0065 × 0074 × 0063 × 002E × 0029 × 2019 × 00A0 × 0074 × 0068 × 0065 ÷
÷ 0065 × 0074 × 0063 × 002E × 0029 × 2019 × 00A0 ÷ 0054 × 0068 × 0065 ÷
÷ 0065 × 0074 × 0063 × 002E × 0029 × 2019 × 00A0 × 2018 × 0028 × 0074 × 0068 × 0065 ÷
÷ 0065 × 0074 × 0063 × 002E × 0029 × 2019 × 00A0 ÷ 2018 × 0028 × 0054 × 0068 × 0065 ÷
÷ 0065 × 0074 × 0063 × 002E × 0029 × 2019 × 00A0 × 0308 × 0074 × 0068 × 0065 ÷
÷ 0065 × 0074 × 0063 × 002E × 0029 × 2019 × 00A0 × 0308 ÷ 0054 × 0068 × 0065 ÷
÷ 0065 × 0074 × 0063 × 002E × 0029 × 2019 × 0308 ÷ 0054 × 0068 × 0065 ÷
÷ 0065 × 0074 × 0063 × 002E × 0029 × 000A ÷ 0308 × 0054 × 0068 × 0065 ÷
÷ 0074 × 0068 × 0065 × 0020 × 0072 × 0065 × 0073 × 0070 × 002E × 0020 × 006C × 0065 × 0061 × 0064 × 0065 × 0072 × 0073 × 0020 × 0061 × 0072 × 0065 ÷
÷ 5B57 × 002E ÷ 5B57 ÷
÷ 0065 × 0074 × 0063 × 002E ÷ 5B83 ÷
÷ 0065 × 0074 × 0063 × 002E × 3002 ÷
÷ 5B57 × 3002 ÷ 5B83 ÷
÷ 0021 × 0020 × 0020 ÷
÷ 0061 × 002E ÷
÷ 0061 × 002E × 000D × 000A ÷
÷ 0061 × 002E × 000D × 000A ÷ 0020 ÷
÷ 0061 × 002E × 000D × 000A ÷ 0061 ÷
÷ 0041 × 002E × 000D × 000A ÷ 0041 ÷
÷ 2060 × 0061 × 2060 × 002E × 2060 × 000D ÷ 2060 × 000A ÷ 2060 ÷
"""


def parse(line: str) -> tuple[str, list[int]]:
    """Turn a test line into the string and the list of its boundaries."""
    chars: list[str] = []
    bounds: list[int] = []
    for tok in line.split():
        if tok == "÷":
            bounds.append(len(chars))
        elif tok == "×":
            pass
        else:
            chars.append(chr(int(tok, 16)))
    return "".join(chars), bounds


def check_lines(lines: str, fn) -> int:
    count = 0
    for line in lines.splitlines():
        s, expected = parse(line)
        assert fn(s) == expected, line
        count += 1
    return count


def test_grapheme_conformance_lines():
    assert check_lines(GRAPHEME_LINES, grapheme_boundaries) >= 70


def test_word_conformance_lines():
    assert check_lines(WORD_LINES, word_boundaries) >= 25


def test_sentence_conformance_lines():
    assert check_lines(SENTENCE_LINES, sentence_boundaries) >= 30


def test_check_values():
    assert len(grapheme_clusters("é")) == 1
    assert len(grapheme_clusters("\r\n")) == 1
    assert len(grapheme_clusters("각")) == 1
    assert len(grapheme_clusters("👨‍👩‍👧")) == 1
    assert grapheme_clusters("🇫🇷🇩🇪") == ["🇫🇷", "🇩🇪"]
    assert len(grapheme_clusters("क्षि")) == 1


def test_legacy_clusters_differ():
    s = "क्षि"
    assert grapheme_boundaries(s) == [0, 4]
    assert grapheme_boundaries(s, extended=False) == [0, 2, 3, 4]


def test_empty_and_single():
    for fn in (grapheme_boundaries, word_boundaries, sentence_boundaries):
        assert fn("") == [0]
        assert fn("a") == [0, 1]


# A brute-force reference for the grapheme rules: each rule is written as a pair of regular
# expressions, one for the text left of the position and one for the text right of it, as in
# UAX 29. Each code point becomes a token of three letters: its GCB value, its InCB value and
# whether it is Extended_Pictographic. The first rule whose two sides match decides.
_G = {"Other": "o", "CR": "r", "LF": "n", "Control": "c", "Extend": "e", "ZWJ": "z",
      "RI": "i", "Prepend": "p", "SpacingMark": "s", "L": "l", "V": "v", "T": "t",
      "LV": "w", "LVT": "x"}
_I = {"None": "-", "Consonant": "C", "Extend": "E", "Linker": "L"}


def _tok(c: str) -> str:
    return _G[gcb(c)] + _I[incb(c)] + ("P" if ext_pict(c) else "-")


def T(g=".", i=".", p=".") -> str:
    return "(?:" + g + i + p + ")"


ANY = T()
_RULES = [
    (T("r") + r"\Z", "^" + T("n"), False),  # GB3
    (T("[crn]") + r"\Z", "", True),  # GB4
    ("", "^" + T("[crn]"), True),  # GB5
    (T("l") + r"\Z", "^" + T("[lvwx]"), False),  # GB6
    (T("[wv]") + r"\Z", "^" + T("[vt]"), False),  # GB7
    (T("[xt]") + r"\Z", "^" + T("t"), False),  # GB8
    ("", "^" + T("[ez]"), False),  # GB9
    ("", "^" + T("s"), False),  # GB9a
    (T("p") + r"\Z", "", False),  # GB9b
    (T(".", "C") + T(".", "[EL]") + "*" + T(".", "L") + T(".", "[EL]") + r"*\Z",
     "^" + T(".", "C"), False),  # GB9c
    (T(".", ".", "P") + T("e") + "*" + T("z") + r"\Z", "^" + T(".", ".", "P"), False),  # GB11
    ("^(?:" + T("i") + T("i") + ")*" + T("i") + r"\Z", "^" + T("i"), False),  # GB12
    ("(?:^|" + "(?!" + T("i") + ")" + ANY + ")(?:" + T("i") + T("i") + ")*" + T("i") + r"\Z",
     "^" + T("i"), False),  # GB13
]


def brute_grapheme_boundaries(s: str) -> list[int]:
    toks = [_tok(c) for c in s]
    n = len(s)
    out = [0] if n else [0]
    for b in range(1, n):
        left, right = "".join(toks[:b]), "".join(toks[b:])
        brk = True
        for lpat, rpat, decision in _RULES:
            if (lpat == "" or re.search(lpat, left)) and (rpat == "" or re.match(rpat, right)):
                brk = decision
                break
        if brk:
            out.append(b)
    if n:
        out.append(n)
    return out


def test_grapheme_against_regex_rules():
    pool = ["\r", "\n", "\x01", "a", " ", "̈", "‍", "‌", "ः", "؀",
            "ᄀ", "ᅠ", "ᆨ", "가", "각", "क", "त", "्",
            "़", "\U0001F1E6", "\U0001F1E7", "⌚", "\U0001F476", "\U0001F3FF"]
    rng = random.Random(29)
    for _ in range(1500):
        s = "".join(rng.choice(pool) for _ in range(rng.randint(0, 9)))
        assert grapheme_boundaries(s) == brute_grapheme_boundaries(s), [hex(ord(c)) for c in s]


def test_boundaries_are_sorted_and_cover_the_text():
    rng = random.Random(45)
    pool = list("aZ1., :'\"\r\n?!()") + ["̈", "‍", "⁠", "א", "〱", "字"]
    for _ in range(500):
        s = "".join(rng.choice(pool) for _ in range(rng.randint(1, 15)))
        for fn in (grapheme_boundaries, word_boundaries, sentence_boundaries):
            b = fn(s)
            assert b[0] == 0 and b[-1] == len(s)
            assert all(b[k] < b[k + 1] for k in range(len(b) - 1))


def test_word_boundary_inside_a_grapheme_cluster():
    # The rules are separate: RI ZWJ RI is one RI pair for words (WB4 drops the ZWJ),
    # but for graphemes the ZWJ ends the first cluster, so the pairs fall differently.
    s, expected = parse("÷ 0061 ÷ 1F1E6 × 200D × 1F1E7 ÷ 1F1E8 ÷ 0062 ÷")
    assert word_boundaries(s) == expected == [0, 1, 4, 5, 6]
    assert grapheme_boundaries(s) == [0, 1, 3, 5, 6]
    others = 0
    for line in WORD_LINES.splitlines():
        s, _ = parse(line)
        if set(word_boundaries(s)) <= set(grapheme_boundaries(s)):
            others += 1
    assert others == len(WORD_LINES.splitlines()) - 1
