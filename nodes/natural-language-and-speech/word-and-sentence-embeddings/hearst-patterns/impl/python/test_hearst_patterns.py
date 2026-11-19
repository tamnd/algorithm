# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hearst-patterns/. The authors are listed in prov/B0F1S5.jsonl.

import random
import re

from hearst_patterns import hearst_matches, hearst_pairs


def items(text: str) -> list:
    """Brackets mark the noun phrases: "[the bow lute] , such as [the Bambara ndang]"."""
    out: list = []
    for part in re.findall(r"\[[^\]]*\]|\S+", text):
        out.append(tuple(part[1:-1].split()) if part.startswith("[") else part)
    return out


def test_hearst_examples() -> None:
    cases = [
        ("[the bow lute] , such as [the Bambara ndang] , is plucked", [("the Bambara ndang", "the bow lute", 1)]),
        ("works by such [authors] as [Herrick] , [Goldsmith] , and [Shakespeare] .",
         [("Herrick", "authors", 2), ("Goldsmith", "authors", 2), ("Shakespeare", "authors", 2)]),
        ("[bruises] , [wounds] , [broken bones] or other [injuries]",
         [("bruises", "injuries", 3), ("wounds", "injuries", 3), ("broken bones", "injuries", 3)]),
        ("[temples] , [treasuries] , and other [important civic buildings] .",
         [("temples", "important civic buildings", 4), ("treasuries", "important civic buildings", 4)]),
        ("[all common-law countries] , including [Canada] and [England]",
         [("Canada", "all common-law countries", 5), ("England", "all common-law countries", 5)]),
        ("[most European countries] , especially [France] , [England] , and [Spain] .",
         [("France", "most European countries", 6), ("England", "most European countries", 6),
          ("Spain", "most European countries", 6)]),
    ]
    for text, want in cases:
        assert hearst_pairs(items(text)) == want


def test_edges() -> None:
    assert hearst_matches([]) == []
    assert hearst_matches(items("such as [dogs]")) == []
    assert hearst_matches(items("[animals] such as")) == []
    assert hearst_matches(items("and other [animals]")) == []
    assert hearst_pairs(items("[animals] SUCH AS [cats] , [dogs] ,")) == [("cats", "animals", 1), ("dogs", "animals", 1)]
    assert hearst_pairs(items("[pets] such as [cats] and [dogs] and [birds]")) == [("cats", "pets", 1), ("dogs", "pets", 1)]
    assert hearst_pairs(items("[cats] , [dogs] and other [pets] , such as [birds]")) == [
        ("cats", "pets", 4), ("dogs", "pets", 4), ("birds", "pets", 1),
    ]


CODE = {",": ",", "such": "s", "as": "a", "and": "&", "or": "|", "other": "o", "including": "i", "especially": "e"}
RIGHT = re.compile(r"N(,N)*(,?[&|]N)?")
LEFT = re.compile(r",?N(,N)*")


def oracle(seq: list) -> list[tuple[int, int, int]]:
    """The same patterns as regular expressions over a one-letter code of the items."""
    enc = "".join("N" if isinstance(x, tuple) else CODE.get(x.lower(), "w") for x in seq)
    out = []

    def nps(start: int, stop: int) -> list[int]:
        return [i for i in range(start, stop) if enc[i] == "N"]

    for p in range(len(enc)):
        before = re.search(r"N,?$", enc[:p])
        h = None if before is None else before.start()
        if enc.startswith("sa", p) and h is not None:
            m = RIGHT.match(enc, p + 2)
            if m:
                out += [(x, h, 1) for x in nps(m.start(), m.end())]
        elif re.match(r"sNa", enc[p:]):
            m = RIGHT.match(enc, p + 3)
            if m:
                out += [(x, p + 1, 2) for x in nps(m.start(), m.end())]
        elif enc[p:p + 1] in ("i", "e") and h is not None:
            m = RIGHT.match(enc, p + 1)
            if m:
                out += [(x, h, 5 if enc[p] == "i" else 6) for x in nps(m.start(), m.end())]
        elif re.match(r"[&|]oN", enc[p:]):
            m = LEFT.match(enc[:p][::-1])
            if m:
                out += [(x, p + 2, 3 if enc[p] == "|" else 4) for x in nps(p - m.end(), p)]
    return out


def test_against_regex_oracle() -> None:
    rng = random.Random(3)
    words = [",", "such", "as", "and", "or", "other", "including", "especially", "the", "is", "Such"]
    triggers = [["such", "as"], ["such", ("np",), "as"], ["and", "other"], ["or", "other"], ["including"], ["especially"]]
    hits = 0
    for _ in range(5000):
        seq = [("np%d" % i,) if rng.random() < 0.45 else rng.choice(words) for i in range(rng.randrange(0, 14))]
        if seq and rng.random() < 0.6:
            p = rng.randrange(len(seq))
            seq[p:p] = rng.choice(triggers)
        got = hearst_matches(seq)
        hits += bool(got)
        assert got == oracle(seq)
        assert len(got) == len(set(got))
        for x, h, k in got:
            assert isinstance(seq[x], tuple) and isinstance(seq[h], tuple) and x != h and 1 <= k <= 6
    assert hits >= 500
