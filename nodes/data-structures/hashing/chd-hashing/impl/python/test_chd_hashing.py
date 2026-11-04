# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chd-hashing/. The authors are listed in prov/X3MZCW.jsonl.

import random

import pytest

from chd_hashing import CHD, P61

S = [10, 22, 37, 40, 52, 60, 70, 72, 75, 88]


def test_page_example() -> None:
    c = CHD(S, random.Random(1), lam=3, p=101)
    assert c.tries == 1 and c.r == 4 and c.m == 10
    assert [c.g(x) for x in S] == [2, 1, 1, 0, 3, 1, 1, 3, 3, 1]
    assert [(c.f1(x), c.f2(x)) for x in (52, 72, 75)] == [(4, 9), (0, 0), (4, 6)]
    assert c.sigma == [0, 0, 0, 21]
    assert {x: c(x) for x in S} == {10: 0, 22: 4, 37: 2, 40: 8, 52: 3, 60: 5, 70: 9, 72: 1, 75: 7, 88: 6}
    assert c.slot(52, 21) == 3 and c.slot(75, 1) == c.slot(52, 1)


def test_edges() -> None:
    c = CHD([], random.Random(0))
    assert c.m == 1 and c(5) == 0
    c = CHD([P61 - 1], random.Random(0))
    assert c(P61 - 1) == 0
    with pytest.raises(ValueError):
        CHD([1, 1])
    with pytest.raises(ValueError):
        CHD([1, 2, 3], m=2)
    with pytest.raises(ValueError):
        CHD([P61])


def test_non_minimal() -> None:
    rng = random.Random(7)
    keys = rng.sample(range(10**6), 300)
    c = CHD(keys, rng, m=330)
    vals = [c(x) for x in keys]
    assert len(set(vals)) == 300 and all(0 <= v < 330 for v in vals)


def test_random_against_dict() -> None:
    rng = random.Random(2009)
    for _ in range(600):
        n = rng.randint(0, 60)
        p = rng.choice([1009, 65521, P61])
        keys = rng.sample(range(p), n)
        lam = rng.randint(1, 6)
        c = CHD(keys, rng, lam=lam, p=p)
        slots = [c(x) for x in keys]
        assert sorted(slots) == list(range(n))  # minimal and perfect
        # use the function as the index of a static dictionary
        oracle = {x: rng.random() for x in keys}
        table: list[float | None] = [None] * c.m
        for x, v in oracle.items():
            table[c(x)] = v
        assert all(table[c(x)] == v for x, v in oracle.items())
        assert all(0 <= c(rng.randrange(p)) < c.m for _ in range(5))
