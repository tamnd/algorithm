# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-fusion/. The authors are listed in prov/R2RS59.jsonl.
import random
from fractions import Fraction

from kernel_fusion import chain_fused, chain_unfused, map_reduce_fused, map_reduce_unfused, occupancy_warps


def sq(v):
    return v * v


def add(a, b):
    return a + b


def test_map_reduce_traffic():
    for seed in range(20):
        rng = random.Random(seed)
        n = rng.randrange(1, 3000)
        b = rng.choice([32, 256, 1024])
        x = [rng.randrange(-100, 100) for _ in range(n)]
        t = -(-n // b)
        s1, m1 = map_reduce_unfused(x, sq, add, b)
        s2, m2 = map_reduce_fused(x, sq, add, b)
        assert s1 == s2 == sum(v * v for v in x)
        assert (m1.reads, m1.writes, m1.launches) == (2 * n + t, n + t + 1, 3)
        assert (m2.reads, m2.writes, m2.launches) == (n + t, t + 1, 2)
        assert (m1.reads + m1.writes) - (m2.reads + m2.writes) == 2 * n


def test_worked_example_ratio():
    n, b = 1 << 20, 256
    t = n // b
    unfused = 3 * n + 2 * t + 1
    fused = n + 2 * t + 1
    assert (unfused, fused) == (3153921, 1056769)
    assert Fraction(unfused, fused) > Fraction(298, 100)


def test_elementwise_chain():
    for k in (1, 2, 5):
        fs = [lambda v, c=c: 3 * v + c for c in range(k)]
        x = list(range(500))
        y1, m1 = chain_unfused(x, fs, 128)
        y2, m2 = chain_fused(x, fs, 128)
        assert y1 == y2
        assert (m1.reads + m1.writes, m1.launches) == (2 * k * 500, k)
        assert (m2.reads + m2.writes, m2.launches) == (2 * 500, 1)


def test_register_pressure_model():
    # assumed SM: 65536 registers, 64 warps, 32 blocks; blocks of 256 threads
    assert occupancy_warps(32, 256) == 64
    assert occupancy_warps(64, 256) == 32
    assert occupancy_warps(128, 256) == 16
    assert occupancy_warps(255, 256) == 8
