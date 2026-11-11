# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hellman-time-memory-tradeoff/. The authors are listed in prov/EQFZ4J.jsonl.

import math
import random

from hellman_time_memory_tradeoff import HellmanTables, hellman_coverage_bound, toy_oneway


def test_inverts_toy_function_20_bits() -> None:
    n = 20
    f = lambda x: toy_oneway(x, n)  # noqa: E731
    m, t, ell = 64, 128, 64  # m t^2 = N; half of Hellman's ell = t tables, to keep the test fast
    rng = random.Random(1980)
    tabs = HellmanTables(f, n, m, t, ell, rng)
    assert tabs.precomputation == m * t * ell
    trials = 60
    found = 0
    for _ in range(trials):
        x = rng.randrange(1 << n)
        y = f(x)
        z = tabs.invert(y)
        if z is not None:
            assert f(z) == y  # a real preimage
            found += 1
    bound = 1 - (1 - hellman_coverage_bound(n, m, t)) ** ell
    # the bound is a lower bound on the coverage; allow sampling noise
    assert found / trials >= bound - 4 * math.sqrt(bound * (1 - bound) / trials)
    assert found >= 15


def test_coverage_of_one_table_matches_bound() -> None:
    n = 16
    f = lambda x: toy_oneway(x, n, key=77)  # noqa: E731
    m, t = 32, 32
    rng = random.Random(5)
    covered_frac = []
    for rep in range(20):
        tabs = HellmanTables(f, n, m, t, 1, rng)
        # count the distinct points x_0 .. x_{t-1} in the kept chains
        covered = set()
        for end, start in tabs.tables[0].items():
            x = start
            for _ in range(t):
                covered.add(x)
                x = tabs.reduce(0, f(x))
        covered_frac.append(len(covered) / (1 << n))
    mean = sum(covered_frac) / len(covered_frac)
    bound = hellman_coverage_bound(n, m, t)
    assert mean >= bound - 0.002
    assert mean <= m * t / (1 << n)


def test_failure_is_none() -> None:
    n = 12
    f = lambda x: toy_oneway(x, n)  # noqa: E731
    tabs = HellmanTables(f, n, 1, 1, 1, random.Random(0))
    misses = sum(tabs.invert(f(x)) is None for x in range(200))
    assert misses > 150


def test_bound_edges() -> None:
    assert hellman_coverage_bound(10, 1, 1) == (1 - 1 / 1024) / 1024
    assert 0 < hellman_coverage_bound(20, 64, 128) <= 64 * 128 / 2**20
