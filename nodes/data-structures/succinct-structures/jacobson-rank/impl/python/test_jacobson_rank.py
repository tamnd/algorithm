# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobson-rank/. The authors are listed in prov/D62R54.jsonl.

import itertools
import random

import pytest

from jacobson_rank import JacobsonRank


def check_all(b: list[int]) -> None:
    r = JacobsonRank(b)
    r.check_invariant()
    pref = list(itertools.accumulate(b, initial=0))
    assert len(r) == len(b)
    for i in range(len(b) + 1):
        assert r.rank1(i) == pref[i]
        assert r.rank0(i) == i - pref[i]
    for i in range(len(b)):
        assert r.access(i) == b[i]
    ones = [i for i, x in enumerate(b) if x]
    for j, p in enumerate(ones, 1):
        assert r.select1(j) == p


def test_page_example() -> None:
    b = [int(c) for c in "1011001011000111"]
    r = JacobsonRank(b)
    assert (r.b, r.s) == (2, 4)
    assert r.X == [1, 3, 0, 1, 3, 0, 2, 3, 0]
    assert r.RB == [0, 1, 3, 3, 0, 2, 2, 3, 0]
    assert r.RS == [0, 4, 9]
    assert r.rank1(13) == 6
    assert r.rank1(16) == 9
    assert r.select1(5) == 8
    check_all(b)


def test_edges() -> None:
    check_all([])
    check_all([1])
    check_all([0])
    check_all([1] * 64)
    check_all([0] * 33)
    check_all([0] * 100 + [1])
    with pytest.raises(IndexError):
        JacobsonRank([0, 0]).select1(1)
    with pytest.raises(IndexError):
        JacobsonRank([1]).rank1(2)


def test_random_against_prefix_sums() -> None:
    rng = random.Random(1989)
    for _ in range(600):
        n = rng.randrange(0, 400)
        p = rng.random()
        check_all([1 if rng.random() < p else 0 for _ in range(n)])
