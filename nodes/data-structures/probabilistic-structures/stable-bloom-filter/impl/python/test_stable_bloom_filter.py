# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stable-bloom-filter/. The authors are listed in prov/XYQ2CR.jsonl.

import random

import pytest

from stable_bloom_filter import Key, StableBloomFilter

POS: dict[Key, list[int]] = {"a": [0, 3], "b": [1, 5], "c": [3, 6], "d": [0, 5], "e": [2, 4], "f": [2, 7]}
STREAM = "abacdefc"
VICTIMS = [[2, 7], [0, 4], [3, 5], [0, 1], [6, 3], [6, 7], [6, 1], [5, 0]]


class FixedSBF(StableBloomFilter):
    def __init__(self) -> None:
        super().__init__(8, 2, d=2, P=2)
        self.script = iter(VICTIMS)

    def _positions(self, key: Key) -> list[int]:
        return POS[key]

    def _victims(self) -> list[int]:
        return next(self.script)


def test_example() -> None:
    f = FixedSBF()
    states = []
    out = []
    for x in STREAM:
        out.append(f.process(x))
        states.append(list(f.cells))
    assert out == [False, False, True, False, True, False, False, False]
    assert states[4] == [3, 2, 0, 2, 0, 3, 2, 0]  # after d, a false positive
    assert states[6] == [3, 1, 3, 2, 3, 3, 0, 3]  # cell 6 of c is now 0
    assert states[7] == [2, 1, 3, 3, 3, 2, 3, 3]  # c was a false negative


def test_edges() -> None:
    f = StableBloomFilter(1, 1, d=1, P=0)
    assert not f.process("x") and f.process("y")  # one cell, never cleared
    assert f.stable_zero_fraction() == 0.0
    g = StableBloomFilter(4, 1, d=1, P=4)
    g.process("x")
    assert g.cells.count(1) == 1  # every cell was decremented, then x was set
    for bad in [dict(m=2, K=3), dict(m=2, K=1, d=0), dict(m=2, K=1, P=3)]:
        with pytest.raises(ValueError):
            StableBloomFilter(**bad)


def test_random_against_model() -> None:
    rng = random.Random(2006)
    for _ in range(500):
        m = rng.randint(1, 30)
        K = rng.randint(1, m)
        d = rng.randint(1, 3)
        P = rng.randint(0, m)
        f = StableBloomFilter(m, K, d, P, seed=rng.randrange(100), rng_seed=rng.randrange(100))
        shadow = random.Random(0)
        shadow.setstate(f.rng.getstate())
        model = [0] * m
        for _ in range(rng.randint(0, 40)):
            x = rng.randrange(15)
            ps = f._positions(x)
            assert len(set(ps)) == K
            want = all(model[p] for p in ps)
            for j in shadow.sample(range(m), P):
                model[j] = max(0, model[j] - 1)
            for p in ps:
                model[p] = f.max
            assert f.process(x) == want
            assert f.cells == model
            assert f.query(x)  # just recorded


def test_stable_fraction() -> None:
    f = StableBloomFilter(2000, 3, d=3, P=50, seed=1, rng_seed=1)
    for x in range(20000):
        f.process(x)
    assert abs(f.zero_fraction() - f.stable_zero_fraction()) < 0.03
    assert abs(f.stable_zero_fraction() - 0.6637) < 0.001
