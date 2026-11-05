# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ppjoin/. The authors are listed in prov/YE460Y.jsonl.

import itertools
import random
from fractions import Fraction

from ppjoin import jaccard, ppjoin

R = ["ABCDE", "ABCDF", "BCDEFG", "AGH", "CDEFH", "ABCDEG"]


def brute(sets, t):
    t = Fraction(t)
    return sorted(
        (i, j)
        for i, j in itertools.combinations(range(len(sets)), 2)
        if set(sets[i]) and set(sets[j]) and jaccard(sets[i], sets[j]) >= t
    )


def test_example() -> None:
    stats: dict = {}
    assert ppjoin(R, "0.6", stats) == [(0, 1), (0, 5), (2, 5)]
    assert stats == {"candidates": 6, "pruned": 3}


def test_edges() -> None:
    assert ppjoin([], "0.5") == []
    assert ppjoin(["", "", "a"], "0.5") == []
    assert ppjoin(["ab", "ba", "ab"], 1) == [(0, 1), (0, 2), (1, 2)]
    assert ppjoin(["abc", "abd"], "0.5") == [(0, 1)]
    assert ppjoin(["abc", "abd"], "0.51") == []
    try:
        ppjoin(["a"], 0)
        raise AssertionError("t = 0 accepted")
    except ValueError:
        pass


def test_random_against_brute_force() -> None:
    rng = random.Random(2008)
    for _ in range(600):
        n = rng.randint(0, 25)
        universe = rng.randint(1, 12)
        sets = [{rng.randrange(universe) for _ in range(rng.randint(0, 8))} for _ in range(n)]
        t = rng.choice(["0.3", "0.5", "0.6", "2/3", "0.75", "0.8", "0.9", "1"])
        assert ppjoin(sets, t) == brute(sets, t)
