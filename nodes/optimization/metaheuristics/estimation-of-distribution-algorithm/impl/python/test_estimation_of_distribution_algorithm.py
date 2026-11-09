# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/estimation-of-distribution-algorithm/. The authors are listed in prov/MH6JW4.jsonl.

import math
import random

from estimation_of_distribution_algorithm import compact_ga, onemax, trap, umda


def test_trap_values() -> None:
    assert trap([1] * 5) == 5 and trap([0] * 5) == 4 and trap([1, 1, 1, 1, 0]) == 0
    assert trap([1] * 5 + [0] * 5) == 9


def test_umda_frequencies_and_margins() -> None:
    n, mu = 20, 8
    for margins in (True, False):
        trace = []
        umda(onemax, n, 16, mu, 40, random.Random(1), margins, trace)
        lo, hi = (1 / n, 1 - 1 / n) if margins else (0.0, 1.0)
        allowed = {min(hi, max(lo, a / mu)) for a in range(mu + 1)}
        for p in trace:
            assert all(lo <= q <= hi for q in p)
            assert all(any(math.isclose(q, v) for v in allowed) for q in p)


def test_without_margins_a_fixed_bit_never_moves() -> None:
    trace = []
    umda(onemax, 30, 10, 5, 60, random.Random(2), False, trace)
    for prev, cur in zip(trace, trace[1:]):
        for a, b in zip(prev, cur):
            if a in (0.0, 1.0):
                assert b == a


def test_genetic_drift_is_a_martingale() -> None:
    # Flat fitness: selection ignores the bits, each p_j is a martingale on {0, 1/10, ..., 1}
    # that is absorbed at 1 with probability p_0 = 1/2.
    trace = []
    umda(lambda x: 0, 400, 20, 10, 300, random.Random(0), False, trace)
    last = trace[-1]
    assert all(q in (0.0, 1.0) for q in last)
    assert abs(sum(last) / 400 - 0.5) < 0.1


def test_invariant_under_increasing_transformation() -> None:
    a = umda(onemax, 20, 16, 8, 30, random.Random(3))
    b = umda(lambda x: math.exp(onemax(x)), 20, 16, 8, 30, random.Random(3))
    assert a[0] == b[0] and a[2] == b[2]


def test_compact_ga_stays_within_margins() -> None:
    n = 20
    trace = []
    compact_ga(onemax, n, 10, 500, random.Random(4), trace)
    assert all(1 / n <= q <= 1 - 1 / n for p in trace for q in p)


def test_fixed_seed_reaches_optimum() -> None:
    best, s, _ = umda(onemax, 50, 40, 20, 100, random.Random(0))
    assert s == 50 and best == [1] * 50
    best, s, _ = compact_ga(onemax, 50, 30, 2000, random.Random(0))
    assert s == 50
