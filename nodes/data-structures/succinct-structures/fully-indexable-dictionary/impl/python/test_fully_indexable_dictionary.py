# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fully-indexable-dictionary/. The authors are listed in prov/ZEDY5H.jsonl.

import bisect
import random

import pytest

from fully_indexable_dictionary import FullyIndexableDictionary


def check_all(u: int, s: set[int]) -> None:
    f = FullyIndexableDictionary(u, s)
    ins = sorted(s)
    outs = [x for x in range(u) if x not in s]
    assert len(f) == len(ins)
    for x in range(u):
        assert f.member(x) == (x in s)
        k = bisect.bisect_right(ins, x)
        assert f.pred(x) == (ins[k - 1] if k else None)
        k = bisect.bisect_left(ins, x)
        assert f.succ(x) == (ins[k] if k < len(ins) else None)
    for r in range(u + 1):
        assert f.rank(r) == bisect.bisect_left(ins, r)
        assert f.rank_out(r) == bisect.bisect_left(outs, r)
    for i, x in enumerate(ins, 1):
        assert f.select(i) == x
    for i, x in enumerate(outs, 1):
        assert f.select_out(i) == x


def test_page_example() -> None:
    s = {0, 2, 3, 6, 8, 9, 13, 14, 15}
    f = FullyIndexableDictionary(16, s)
    assert not f.member(7)
    assert f.rank(10) == 6
    assert f.select(4) == 6
    assert f.pred(12) == 9
    assert f.succ(10) == 13
    assert f.succ(15) == 15
    assert f.pred(1) == 0
    assert f.rank_out(10) == 4
    assert f.select_out(5) == 10
    check_all(16, s)


def test_edges() -> None:
    check_all(0, set())
    check_all(1, set())
    check_all(1, {0})
    check_all(64, set(range(64)))
    check_all(700, {699})
    check_all(1100, {0, 1099})
    f = FullyIndexableDictionary(10, {5})
    assert f.pred(4) is None and f.succ(6) is None
    with pytest.raises(IndexError):
        f.select(2)
    with pytest.raises(ValueError):
        FullyIndexableDictionary(10, {10})


def test_random_against_sorted_lists() -> None:
    rng = random.Random(2002)
    for _ in range(500):
        u = rng.randrange(0, 1200 if rng.random() < 0.1 else 200)
        p = rng.random()
        check_all(u, {x for x in range(u) if rng.random() < p})
