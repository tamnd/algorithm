# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/revolving-door-ordering/. The authors are listed in prov/JJSYG3.jsonl.

import itertools
import random
from math import comb

import pytest

from revolving_door_ordering import rank, revolving_door, revolving_door_subsets, unrank


def reference(n: int, k: int) -> list[tuple[int, ...]]:
    """Reference: the weight-k strings of the reflected Gray code, in its order."""
    out = []
    for i in range(1 << n):
        g = i ^ (i >> 1)
        if bin(g).count("1") == k:
            out.append(tuple(j + 1 for j in range(n) if g >> j & 1))
    return out


def test_example() -> None:
    got = ["".join(map(str, s)) for s in revolving_door_subsets(5, 3)]
    assert got == ["123", "134", "234", "124", "145", "245", "345", "135", "235", "125"]
    assert rank((2, 4, 5)) == 5
    assert unrank(5, 5, 3) == (2, 4, 5)


def test_knuth_list() -> None:
    # Knuth, Section 7.2.1.3, (27): index lists c3 c2 c1 over {0..5}.
    want = "210 320 321 310 430 431 432 420 421 410 540 541 542 543 530 531 532 520 521 510".split()
    got = ["".join(str(e - 1) for e in sorted(s, reverse=True)) for s in revolving_door_subsets(6, 3)]
    assert got == want


def test_edges() -> None:
    assert revolving_door_subsets(0, 0) == [()]
    assert revolving_door_subsets(4, 0) == [()]
    assert revolving_door_subsets(4, 4) == [(1, 2, 3, 4)]
    assert revolving_door_subsets(3, 5) == []
    assert revolving_door_subsets(3, -1) == []
    assert rank(()) == 0
    assert unrank(0, 3, 0) == ()
    with pytest.raises(ValueError):
        list(revolving_door(-1, 0))
    with pytest.raises(ValueError):
        unrank(10, 5, 3)


def test_matches_gray_restriction_and_door_property() -> None:
    for n in range(0, 12):
        for k in range(0, n + 1):
            lst = revolving_door_subsets(n, k)
            assert lst == reference(n, k)
            assert len(lst) == comb(n, k) and len(set(lst)) == len(lst)
            assert set(lst) == set(itertools.combinations(range(1, n + 1), k))
            for u, v in zip(lst, lst[1:]):
                assert len(set(u) ^ set(v)) == 2
            if 0 < k < n:
                assert lst[0] == tuple(range(1, k + 1))
                assert lst[-1] == tuple(range(1, k)) + (n,)


def test_rank_unrank_random() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randrange(1, 25)
        k = rng.randrange(0, n + 1)
        r = rng.randrange(comb(n, k))
        s = unrank(r, n, k)
        assert rank(s) == r
    for n in range(0, 10):
        for k in range(0, n + 1):
            for r, s in enumerate(revolving_door_subsets(n, k)):
                assert rank(s) == r and unrank(r, n, k) == s
