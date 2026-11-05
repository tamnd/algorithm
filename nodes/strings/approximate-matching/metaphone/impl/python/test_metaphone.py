# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metaphone/. The authors are listed in prov/SN7VAT.jsonl.

import random
import re

from metaphone import metaphone

# The rule table of the page, one regular expression for each case, tried in order.
RULES = [
    (r"^[AEIOU]", None), (r"[AEIOU]", ""),
    (r"(?<=M)B$", ""), (r"B", "B"),
    (r"(?<=S)CH", "K"), (r"C(?=IA|H)", "X"), (r"C(?=[IEY])", "S"), (r"C", "K"),
    (r"D(?=G[EYI])", "J"), (r"D", "T"),
    (r"G(?=H[^AEIOU])", ""), (r"G(?=N$|NED$)", ""), (r"(?<=D)G(?=[EIY])", ""),
    (r"G(?=[IEY])", "J"), (r"G", "K"),
    (r"(?<=[CGPST])H", ""), (r"(?<=^W)H", ""), (r"(?<=[AEIOU])H(?![AEIOU])", ""), (r"H", "H"),
    (r"(?<=C)K", ""), (r"K", "K"),
    (r"P(?=H)", "F"), (r"P", "P"), (r"Q", "K"),
    (r"S(?=H|IO|IA)", "X"), (r"S", "S"),
    (r"T(?=IA|IO)", "X"), (r"T(?=H)", "0"), (r"T(?=CH)", ""), (r"T", "T"),
    (r"V", "F"),
    (r"^W(?=H)", "W"), (r"W(?=[AEIOU])", "W"), (r"W", ""),
    (r"^X", "S"), (r"X", "KS"),
    (r"Y(?=[AEIOU])", "Y"), (r"Y", ""), (r"Z", "S"),
    (r"[FJLMNR]", None),
]
COMPILED = [(re.compile(p), out) for p, out in RULES]


def by_table(word: str) -> str:
    s = [c for c in word.upper() if "A" <= c <= "Z"]
    w = "".join(c for i, c in enumerate(s) if i == 0 or c != s[i - 1] or c == "C")
    if w[:2] in ("KN", "GN", "PN", "AE", "WR"):
        w = w[1:]
    out = []
    for i in range(len(w)):
        for pat, code in COMPILED:
            if pat.match(w, i):
                out.append(w[i] if code is None else code)
                break
        else:
            raise AssertionError("no rule for " + w[i])
    return "".join(out)


EXAMPLES = {
    "Knight": "NT", "Wright": "RT", "Thumb": "0M", "Philips": "FLPS", "Phillips": "FLPS",
    "Smith": "SM0", "Smyth": "SM0", "Catherine": "K0RN", "Kathryn": "K0RN",
    "Xavier": "SFR", "White": "WT", "Nation": "NXN", "Judge": "JJ", "Gnome": "NM",
    "Sign": "SN", "Signed": "SNT", "Thompson": "0MPSN", "Tomson": "TMSN",
    "Taylor": "TLR", "Tailor": "TLR", "Michael": "MXL", "Chris": "XRS", "Karl": "KRL",
    "Carl": "KRL", "Stephen": "STFN", "Steven": "STFN", "Aeon": "EN", "Science": "SSNS",
}


def test_examples() -> None:
    for word, want in EXAMPLES.items():
        assert metaphone(word) == want
        assert by_table(word) == want


def test_edges() -> None:
    assert metaphone("") == ""
    assert metaphone("123") == ""
    assert metaphone("a") == "A"
    assert metaphone("x") == "S"
    assert metaphone("h") == "H"
    assert metaphone("o'Brien") == metaphone("OBRIEN")


def test_random_against_table() -> None:
    rng = random.Random(1990)
    for letters in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "CGHSTI", "AEGHNDW", "BMPHTCIAO"):
        for _ in range(800):
            word = "".join(rng.choice(letters) for _ in range(rng.randint(1, 10)))
            got = metaphone(word)
            assert got == by_table(word)
            assert all(c in "0BFHJKLMNPRSTWXY" for c in got[1:])
            doubled = "".join(c + c if c != "C" else c for c in word)
            assert metaphone(doubled) == got
