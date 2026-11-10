# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warp-specialization/. The authors are listed in prov/G81808.jsonl.
import random
from fractions import Fraction as F

from warp_specialization import (
    register_split, specialized, specialized_time, uniform_time, unspecialized_time,
)


def test_ring_invariants():
    rng = random.Random(2)
    for _ in range(200):
        T = rng.randrange(1, 30)
        k = rng.randrange(1, 5)
        load = [F(rng.randrange(1, 20)) for _ in range(T)]
        comp = [F(rng.randrange(1, 20)) for _ in range(T)]
        ls, le, cs, ce = specialized(load, comp, k)
        for t in range(T):
            assert cs[t] >= le[t]                       # compute after the load
            if t >= k:
                assert ls[t] >= ce[t - k]               # never overwrite a buffer in use
            if t:
                assert cs[t] >= ce[t - 1] and ls[t] >= le[t - 1]
        total = specialized_time(load, comp, k)
        assert total >= max(sum(load), sum(comp))
        assert total <= unspecialized_time(load, comp)
        assert specialized_time(load, comp, k + 1) <= total
        if k == 1:
            assert total == unspecialized_time(load, comp)


def test_uniform_formula():
    for T in range(1, 12):
        for L in (1, 3, 5):
            for C in (1, 4):
                for k in (1, 2, 3):
                    assert specialized_time([L] * T, [C] * T, k) == uniform_time(T, L, C, k)


def test_worked_example():
    # 8 tiles; a load takes 3 units and a compute 4 units
    assert unspecialized_time([3] * 8, [4] * 8) == 56
    assert specialized_time([3] * 8, [4] * 8, 1) == 56
    assert specialized_time([3] * 8, [4] * 8, 2) == 3 + 8 * 4 == 35
    assert F(56, 35) == F(8, 5)


def test_register_split():
    # assumed: 65536 registers; one producer warp group of 128 threads, two consumer groups of 256 threads
    assert 65536 // 384 == 170
    assert register_split(65536, 128, 256, 40) == 236
    assert register_split(65536, 128, 256, 24) == 244
