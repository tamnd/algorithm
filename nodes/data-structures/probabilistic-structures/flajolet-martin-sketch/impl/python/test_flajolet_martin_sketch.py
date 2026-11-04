# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flajolet-martin-sketch/. The authors are listed in prov/86TWSR.jsonl.

import random

import pytest

from flajolet_martin_sketch import PHI, FMSketch, Key, rho

HASHES: dict[Key, int] = {"a": 12, "b": 7, "c": 4, "d": 16, "e": 9, "f": 2, "g": 11}


class FixedFM(FMSketch):
    def _hash(self, key: Key) -> int:
        return HASHES[key]


def test_example() -> None:
    s = FixedFM(m=2, L=8)
    for k in "abcadefgb":
        s.add(k)
    assert s.bitmaps == [0b1011, 0b101]
    assert s.rank(0) == 2 and s.rank(1) == 1
    assert s.estimate() == pytest.approx(2 / PHI * 2 ** 1.5)
    assert round(s.estimate(), 2) == 7.31


def test_edges() -> None:
    assert rho(1) == 0 and rho(8) == 3 and rho(12) == 2
    s = FMSketch(m=1, L=4)
    assert s.rank(0) == 0
    s.bitmaps[0] = 0b1111
    assert s.rank(0) == 4
    with pytest.raises(ValueError):
        FMSketch(m=0)
    with pytest.raises(ValueError):
        FMSketch(m=2).merge(FMSketch(m=4))


def brute(keys: set[int], m: int, L: int, seed: int) -> list[int]:
    s = FMSketch(m, L, seed)
    bm = [0] * m
    for x in keys:
        y = s._hash(x)
        j, q = y % m, y // m
        for r in range(L):
            if q and q % (1 << (r + 1)) == (1 << r):
                bm[j] |= 1 << r
    return bm


def test_random_set_function() -> None:
    rng = random.Random(1985)
    for _ in range(500):
        m, L, seed = rng.randint(1, 8), rng.randint(1, 12), rng.randrange(50)
        keys = {rng.randrange(1000) for _ in range(rng.randint(0, 40))}
        stream = [x for x in keys for _ in range(rng.randint(1, 3))]
        rng.shuffle(stream)
        a = FMSketch(m, L, seed)
        for x in stream:
            a.add(x)
        assert a.bitmaps == brute(keys, m, L, seed)
        part = set(rng.sample(sorted(keys), len(keys) // 2))
        b, c = FMSketch(m, L, seed), FMSketch(m, L, seed)
        for x in part:
            b.add(x)
        for x in keys - part:
            c.add(x)
        assert b.merge(c).bitmaps == a.bitmaps
        assert b.merge(c).estimate() == a.estimate()


def test_accuracy() -> None:
    errs = []
    for seed in range(10):
        s = FMSketch(m=64, L=32, seed=seed)
        n = 20000
        for i in range(n):
            s.add(i)
        errs.append(s.estimate() / n - 1)
    assert all(abs(e) < 0.4 for e in errs)
    assert abs(sum(errs) / len(errs)) < 0.15
