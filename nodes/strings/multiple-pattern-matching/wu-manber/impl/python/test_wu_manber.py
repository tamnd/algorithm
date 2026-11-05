# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wu-manber/. The authors are listed in prov/2AQSRW.jsonl.

import random

import pytest

from wu_manber import build_tables, wu_manber


def naive(t, pats) -> list[tuple[int, int]]:
    out = []
    for j, q in enumerate(pats):
        for s in range(len(t) - len(q) + 1):
            if t[s : s + len(q)] == q:
                out.append((s, j))
    return sorted(out)


EXAMPLE_TEXT = "fastsearchforpatternsinlongtext"
EXAMPLE_PATTERNS = ["search", "pattern", "tern", "text", "barn"]


def test_example_tables() -> None:
    lmin, b, shift, hash_table, prefix = build_tables(EXAMPLE_PATTERNS, 2)
    assert (lmin, b) == (4, 2)
    want = {"ar": 0, "rn": 0, "tt": 0, "xt": 0, "at": 1, "ea": 1, "er": 1, "ex": 1, "ba": 2, "pa": 2, "se": 2, "te": 2}
    assert shift == {tuple(k): v for k, v in want.items()}
    assert hash_table == {("a", "r"): [0], ("t", "t"): [1], ("r", "n"): [2, 4], ("x", "t"): [3]}
    assert prefix[4] == ("b", "a")


def test_example_search() -> None:
    stats: dict[str, int] = {}
    got = wu_manber(EXAMPLE_TEXT, EXAMPLE_PATTERNS, 2, stats)
    assert got == [(4, 0), (13, 1), (16, 2), (27, 3)]
    assert stats == {"windows": 14, "zero": 4, "compares": 4}


def test_small_cases() -> None:
    assert wu_manber("", []) == []
    assert wu_manber("", [""]) == [(0, 0)]
    assert wu_manber("ab", ["", "x", "abc"]) == [(0, 0), (1, 0), (2, 0)]
    assert wu_manber("ushers", ["he", "she", "his", "hers"]) == [(1, 1), (2, 0), (2, 3)]
    assert wu_manber("aaaa", ["aa", "a", "aa"], 3) == naive("aaaa", ["aa", "a", "aa"])
    assert wu_manber([1, 2, 1, 2], [[2, 1], [1, 2, 1]]) == [(0, 1), (1, 0)]
    with pytest.raises(ValueError):
        wu_manber("abc", ["a"], 0)


def test_shift_is_largest_safe() -> None:
    # SHIFT[X] is the smallest distance from the end of a truncated pattern to an end of X.
    rng = random.Random(9)
    for _ in range(300):
        pats = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 6))) for _ in range(rng.randint(1, 4))]
        for block in (1, 2, 3):
            lmin, b, shift, _, _ = build_tables(pats, block)
            for x in {tuple(q[i : i + b]) for q in pats for i in range(len(q) - b + 1)}:
                want = lmin - b + 1
                for q in pats:
                    for e in range(b, lmin + 1):
                        if tuple(q[e - b : e]) == x:
                            want = min(want, lmin - e)
                assert shift.get(x, lmin - b + 1) == want


def random_text(rng: random.Random, sigma: int, n: int) -> str:
    kind = rng.randrange(3)
    if kind == 0:
        return "".join(rng.choice("abcd"[:sigma]) for _ in range(n))
    period = "".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randint(1, 4)))
    s = (period * (n // len(period) + 1))[:n]
    if kind == 2 and n > 0:
        i = rng.randrange(n)
        s = s[:i] + rng.choice("abcd"[:sigma]) + s[i + 1 :]
    return s


def random_patterns(rng: random.Random, t: str, sigma: int) -> list[str]:
    pats: list[str] = []
    for _ in range(rng.randint(1, 6)):
        kind = rng.randrange(5)
        if kind == 0 and t:
            i = rng.randrange(len(t))
            pats.append(t[i : i + rng.randint(1, 7)])
        elif kind == 1 and pats:
            q = rng.choice(pats)
            pats.append(q[: rng.randint(0, len(q))])  # a prefix of another pattern
        elif kind == 2 and pats:
            q = rng.choice(pats)
            pats.append(q[rng.randint(0, len(q)) :])  # a suffix of another pattern
        elif kind == 3 and pats:
            pats.append(rng.choice(pats))  # a pattern listed twice
        else:
            pats.append(random_text(rng, sigma, rng.randint(0, 7)))
    return pats


def test_random_against_naive() -> None:
    rng = random.Random(20261106)
    cases = 0
    for sigma in (1, 2, 4):
        for _ in range(250):
            t = random_text(rng, sigma, rng.randint(0, 40))
            pats = random_patterns(rng, t, sigma)
            want = naive(t, pats)
            for block in (1, 2, 3, 4):
                assert wu_manber(t, pats, block) == want
                cases += 1
    assert cases >= 500
