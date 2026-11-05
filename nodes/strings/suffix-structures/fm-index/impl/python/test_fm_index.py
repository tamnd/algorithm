# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fm-index/. The authors are listed in prov/BSBQWW.jsonl.

import random

from fm_index import FMIndex


def naive_bwt(text: str) -> str:
    t = text + "\0"
    rows = sorted(range(len(t)), key=lambda i: t[i:])
    return "".join("$" if t[i - 1] == "\0" else t[i - 1] for i in rows)


def naive_locate(text: str, pattern: str) -> list[int]:
    return [i for i in range(len(text) - len(pattern) + 1) if text[i:i + len(pattern)] == pattern]


def bwt_string(fm: FMIndex) -> str:
    return "".join("$" if x == 0 else fm.symbols[x - 1] for x in fm.bwt)


def test_banana() -> None:
    fm = FMIndex("banana", step=2, block=4)
    assert bwt_string(fm) == "annb$aa"
    assert fm.c == [0, 1, 4, 5, 7]
    assert fm._range("ana") == (2, 4)
    assert fm.count("ana") == 2 and fm.locate("ana") == [1, 3]
    assert fm.count("nab") == 0 and fm.count("x") == 0
    assert fm.extract(1, 4) == list("ana")


def test_mississippi() -> None:
    fm = FMIndex("mississippi")
    assert bwt_string(fm) == naive_bwt("mississippi") == "ipssm$pissii"
    assert fm.locate("ssi") == [2, 5]
    assert fm.locate("i") == [1, 4, 7, 10]
    assert "".join(fm.extract(0, 11)) == "mississippi"


def test_empty_and_special() -> None:
    fm = FMIndex("")
    assert fm.count("") == 1 and fm.count("a") == 0 and fm.extract(0, 0) == []
    for n in range(1, 30):
        for text in ("a" * n, "ab" * n):
            fm = FMIndex(text, step=3, block=5)
            assert bwt_string(fm) == naive_bwt(text)
            for pat in ("a", "aa", "ab", "ba", "aba", "b" * 2):
                assert fm.locate(pat) == naive_locate(text, pat)


def test_random() -> None:
    rng = random.Random(7)
    for trial in range(800):
        sigma = (1, 2, 4)[trial % 3]
        n = rng.randrange(0, 40)
        text = "".join(rng.choice("acgt"[:sigma]) for _ in range(n))
        fm = FMIndex(text, step=rng.randrange(1, 6), block=rng.randrange(1, 9))
        assert bwt_string(fm) == naive_bwt(text)
        for _ in range(5):
            m = rng.randrange(1, 6)
            pat = "".join(rng.choice("acgt"[:sigma + 1] if sigma < 4 else "acgt") for _ in range(m))
            assert fm.count(pat) == len(naive_locate(text, pat))
            assert fm.locate(pat) == naive_locate(text, pat)
        a = rng.randrange(0, n + 1)
        b = rng.randrange(a, n + 1)
        assert "".join(fm.extract(a, b)) == text[a:b]
