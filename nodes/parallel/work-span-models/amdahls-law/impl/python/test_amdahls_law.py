# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amdahls-law/. The authors are listed in prov/W8TH5A.jsonl.

import random
from fractions import Fraction as F

from amdahls_law import (amdahl_efficiency, amdahl_limit, amdahl_speedup, amdahl_time,
                         half_limit_processors, karp_flatt, serial_then_parallel_greedy_time)


def fractions(rng, k):
    yield F(0)
    yield F(1)
    for _ in range(k):
        d = rng.randint(1, 1000)
        yield F(rng.randint(0, d), d)


def test_formula_and_edge_cases():
    assert amdahl_speedup(F(95, 100), 8) == F(160, 27)  # about 5.926
    assert amdahl_limit(F(95, 100)) == 20
    assert amdahl_limit(1) is None
    for p in range(1, 50):
        assert amdahl_speedup(0, p) == 1
        assert amdahl_speedup(1, p) == p
    rng = random.Random(1)
    for f in fractions(rng, 200):
        assert amdahl_speedup(f, 1) == 1
        assert amdahl_speedup(f, 4) == 1 / ((1 - f) + f / 4)


def test_bounds_and_monotonicity():
    rng = random.Random(2)
    for f in fractions(rng, 200):
        prev = F(0)
        for p in (1, 2, 3, 5, 8, 64, 1000):
            s = amdahl_speedup(f, p)
            assert 1 <= s <= p
            assert s >= prev
            prev = s
            if f < 1:
                assert s < amdahl_limit(f) or (f == 0 and s == 1)
            assert amdahl_efficiency(f, p) <= 1


def test_half_of_the_limit():
    rng = random.Random(3)
    for f in fractions(rng, 200):
        if 0 < f < 1:
            p = half_limit_processors(f)
            assert 1 / ((1 - f) + f / p) == amdahl_limit(f) / 2
    assert half_limit_processors(F(95, 100)) == 19


def test_karp_flatt_recovers_serial_fraction():
    rng = random.Random(4)
    for f in fractions(rng, 200):
        for p in (2, 3, 16, 100):
            assert karp_flatt(amdahl_speedup(f, p), p) == 1 - f


def test_greedy_schedule_of_serial_then_parallel_program():
    # a chain of a nodes, then b independent nodes: T_1 = a + b, f = b / (a + b)
    rng = random.Random(5)
    for _ in range(300):
        a, b, p = rng.randint(0, 50), rng.randint(0, 500), rng.randint(1, 40)
        if a + b == 0:
            continue
        t1 = a + b
        f = F(b, t1)
        tp = serial_then_parallel_greedy_time(a, b, p)
        assert tp >= amdahl_time(f, p, t1)
        assert F(t1, tp) <= amdahl_speedup(f, p)
        if b % p == 0:
            assert tp == amdahl_time(f, p, t1)
