# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rank-select-dictionary/. The authors are listed in prov/P99JRP.jsonl.

import itertools
import random

import pytest

from rank_select_dictionary import RankSelectDictionary


def check_all(b: list[int], params: tuple[int, int, int, int] | None = None) -> None:
    d = RankSelectDictionary(b, params)
    pref = list(itertools.accumulate(b, initial=0))
    assert len(d) == len(b)
    for i in range(len(b)):
        assert d.access(i) == b[i]
    for i in range(len(b) + 1):
        assert d.rank1(i) == pref[i]
        assert d.rank0(i) == i - pref[i]
    for j, p in enumerate([i for i, x in enumerate(b) if x], 1):
        assert d.select1(j) == p
    for j, p in enumerate([i for i, x in enumerate(b) if not x], 1):
        assert d.select0(j) == p


def test_page_example() -> None:
    b = [int(c) for c in "10110010110001110000000001"]
    d = RankSelectDictionary(b, (4, 7, 2, 3))
    ix = d.sel1
    assert ix.G == [0, 8, 15]
    assert ix.sparse == [False, False, True]
    assert ix.S[0] == [0, 3] and ix.S[1] == [0, 5]
    assert ix.E2[0] == [None, [3, 6]]
    assert ix.E1[2] == [15, 25]
    assert [d.select1(j) for j in (4, 6, 8, 10)] == [6, 9, 14, 25]
    check_all(b, (4, 7, 2, 3))


def test_edges() -> None:
    check_all([])
    check_all([1])
    check_all([0])
    check_all([1] * 200)
    check_all([0] * 130 + [1])
    check_all([1] + [0] * 300 + [1], (2, 50, 1, 1))
    with pytest.raises(IndexError):
        RankSelectDictionary([0, 0]).select1(1)
    with pytest.raises(IndexError):
        RankSelectDictionary([1, 1]).select0(1)


def test_random_default_parameters() -> None:
    rng = random.Random(1996)
    for _ in range(300):
        n = rng.randrange(0, 700)
        p = rng.random() ** 2
        check_all([1 if rng.random() < p else 0 for _ in range(n)])


def test_random_small_parameters() -> None:
    rng = random.Random(7)
    for _ in range(400):
        n = rng.randrange(0, 300)
        p = rng.random()
        k2 = rng.randrange(1, 4)
        params = (k2 * rng.randrange(1, 4), rng.randrange(1, 60), k2, rng.randrange(1, 20))
        check_all([1 if rng.random() < p else 0 for _ in range(n)], params)
