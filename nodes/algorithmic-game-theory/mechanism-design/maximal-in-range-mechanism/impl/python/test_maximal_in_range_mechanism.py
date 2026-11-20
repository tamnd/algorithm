# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-in-range-mechanism/. The authors are listed in prov/HD9BNP.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from maximal_in_range_mechanism import (
    all_allocations,
    grand_or_single_range,
    maximal_in_range,
    value,
    welfare,
)

F = Fraction


def subsets(m):
    return [frozenset(c) for k in range(m + 1) for c in combinations(range(m), k)]


def additive(item_values):
    m = len(item_values)
    return {s: sum((F(item_values[j]) for j in s), F(0)) for s in subsets(m)}


def random_xos(rng, m, clauses=3, hi=6):
    """Maximum of a few additive functions. Such valuations are subadditive."""
    parts = [[rng.randint(0, hi) for _ in range(m)] for _ in range(clauses)]
    return {s: max(sum((F(p[j]) for j in s), F(0)) for p in parts) for s in subsets(m)}


def test_worked_example():
    bids = [additive([3, 3, 3, 3]), additive([5, 1, 1, 1])]
    rng = grand_or_single_range(2, 4)
    x, p = maximal_in_range(rng, bids)
    assert x == (0, 0, 0, 0)
    assert welfare(bids, x) == 12
    assert p == [F(8), F(0)]
    opt = max(welfare(bids, o) for o in all_allocations(2, 4))
    assert opt == 14


def test_full_range_is_vcg():
    gen = random.Random(1)
    for _ in range(30):
        n, m = gen.randint(1, 3), gen.randint(1, 3)
        bids = [random_xos(gen, m) for _ in range(n)]
        rng = all_allocations(n, m)
        x, p = maximal_in_range(rng, bids)
        assert welfare(bids, x) == max(welfare(bids, o) for o in rng)
        for i in range(n):
            assert p[i] >= 0
            assert value(bids[i], x, i) - p[i] >= 0


def test_dsic_by_brute_force():
    gen = random.Random(2)
    for _ in range(12):
        n, m = gen.randint(2, 3), gen.randint(2, 3)
        rng = grand_or_single_range(n, m)
        others = [random_xos(gen, m) for _ in range(n)]
        types = [random_xos(gen, m) for _ in range(8)]
        for i in range(n):
            results = []
            for report in types:
                bids = list(others)
                bids[i] = report
                x, p = maximal_in_range(rng, bids)
                results.append((x, p[i]))
            for t, true in enumerate(types):
                x0, p0 = results[t]
                honest = value(true, x0, i) - p0
                for x, pay in results:
                    assert honest >= value(true, x, i) - pay


def test_ratio_at_most_two_sqrt_m():
    gen = random.Random(3)
    for _ in range(40):
        n, m = gen.randint(1, 3), gen.randint(1, 4)
        vals = [random_xos(gen, m) for _ in range(n)]
        x, _ = maximal_in_range(grand_or_single_range(n, m), vals)
        got = welfare(vals, x)
        opt = max(welfare(vals, o) for o in all_allocations(n, m))
        assert got <= opt
        assert opt * opt <= 4 * m * got * got


def test_range_does_not_depend_on_bids():
    rng = grand_or_single_range(2, 2)
    assert len(rng) == len(set(rng))
    assert (0, 0) in rng and (1, 1) in rng and (0, 1) in rng and (None, None) in rng
    assert (0, 0, 1) not in grand_or_single_range(2, 3)
    try:
        maximal_in_range([], [additive([1])])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
