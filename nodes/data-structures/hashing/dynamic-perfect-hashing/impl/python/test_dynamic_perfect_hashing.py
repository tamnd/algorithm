# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-perfect-hashing/. The authors are listed in prov/F7B69T.jsonl.

import random

import pytest

from dynamic_perfect_hashing import P61, DynamicPerfectHash


def state(d: DynamicPerfectHash) -> tuple:
    return d.M, d.u, [sorted(b) for b in d.buckets], list(d.L), sum(len(t) for t in d.tables)


def test_page_example() -> None:
    d = DynamicPerfectHash(random.Random(5), p=101)
    got = []
    for x in [10, 22, 37, 40, 52, 60, 70]:
        d.insert(x)
        d.check_invariant()
        got.append(state(d))
    assert got[1] == (2, 0, [[22], [10]], [2, 2], 16)
    assert got[3] == (4, 0, [[40], [10, 22], [], [37]], [2, 4, 2, 2], 56)
    assert got[5] == (4, 2, [[40, 52, 60], [10, 22], [], [37]], [4, 4, 2, 2], 80)
    assert got[6][0] == 7 and got[6][1] == 0 and got[6][4] == 144
    d.delete(37)
    d.check_invariant()
    assert d.search(22) and not d.search(37) and len(d) == 6


def test_edges() -> None:
    d = DynamicPerfectHash(random.Random(1))
    assert not d.search(0) and len(d) == 0
    d.delete(5)
    d.insert(5)
    d.insert(5)
    assert len(d) == 1 and d.search(5)
    d.delete(5)
    assert len(d) == 0 and not d.search(5)
    for x in [0, P61 - 1, 2**40]:
        d.insert(x)
    d.check_invariant()
    assert d.search(P61 - 1) and d.search(0)
    with pytest.raises(ValueError):
        d.insert(P61)


def test_insert_delete_same_key_many_times() -> None:
    d = DynamicPerfectHash(random.Random(2), p=1009)
    for x in range(20):
        d.insert(x)
    for _ in range(500):
        d.delete(3)
        d.insert(3)
        d.check_invariant()
    assert d.keys() == set(range(20))


def test_random_against_set() -> None:
    rng = random.Random(1994)
    for _ in range(600):
        p = rng.choice([101, 1009, P61])
        d = DynamicPerfectHash(rng, p=p)
        model: set[int] = set()
        universe = rng.randint(1, 80)
        for _ in range(rng.randint(0, 80)):
            x = rng.randrange(universe)
            r = rng.random()
            if r < 0.5:
                d.insert(x)
                model.add(x)
            elif r < 0.8:
                d.delete(x)
                model.discard(x)
            else:
                assert d.search(x) == (x in model)
            d.check_invariant()
        assert d.keys() == model
        assert all(d.search(x) == (x in model) for x in range(universe))
