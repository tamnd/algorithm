# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reproducible-summation/. The authors are listed in prov/R755YZ.jsonl.

import itertools
import math
import random
from fractions import Fraction

from reproducible_summation import (P, boundaries, fold_partials, merge_partials,
                                    reproducible_sum)


def gamma(k):
    u = Fraction(1, 2 ** P)
    return k * u / (1 - k * u)


def data(rng, n, spread):
    return [rng.uniform(-1, 1) * 10.0 ** rng.randint(-spread, spread) for _ in range(n)]


def test_small_example():
    xs = [1e16, 1.0, -1e16, 1.0]
    for p in itertools.permutations(xs):
        assert reproducible_sum(p) == 2.0


def test_permutation_invariance():
    rng = random.Random(11)
    for trial in range(30):
        xs = data(rng, rng.randint(1, 400), rng.randint(0, 20))
        want = reproducible_sum(xs)
        for _ in range(5):
            rng.shuffle(xs)
            assert reproducible_sum(xs) == want


def test_partition_invariance():
    rng = random.Random(12)
    for trial in range(30):
        xs = data(rng, 300, 12)
        want = reproducible_sum(xs)
        cuts = sorted(rng.sample(range(1, 300), rng.randint(1, 8)))
        parts = [xs[i:j] for i, j in zip([0] + cuts, cuts + [300])]
        assert merge_partials(parts) == want


def test_levels_are_exact():
    rng = random.Random(13)
    for trial in range(40):
        xs = data(rng, rng.randint(1, 200), 15)
        m = max(abs(x) for x in xs)
        Ms = boundaries(m, len(xs), 3)
        T = fold_partials(xs, Ms)
        # Recompute with exact arithmetic: each extraction and each T_j is exact.
        exact = [Fraction(0)] * len(Ms)
        tail = Fraction(0)
        for x in xs:
            v = x
            for j, M in enumerate(Ms):
                q = (M + v) - M
                assert Fraction(v) - Fraction(q) == Fraction(v - q)
                assert M == 0.0 or abs(v) <= M / (2 * len(xs))
                exact[j] += Fraction(q)
                v = v - q
            tail += Fraction(v)
        assert [Fraction(t) for t in T] == exact
        assert sum(exact) + tail == sum(Fraction(x) for x in xs)


def test_error_bound():
    rng = random.Random(14)
    for K in (1, 2, 3):
        for trial in range(30):
            n = rng.randint(1, 500)
            xs = data(rng, n, 10)
            m = max(abs(x) for x in xs)
            Ms = boundaries(m, n, K)
            T = fold_partials(xs, Ms)
            S = sum(Fraction(x) for x in xs)
            err = abs(Fraction(reproducible_sum(xs, K)) - S)
            bound = n * Fraction(Ms[-1]) / 2 ** P + gamma(len(T) - 1) * sum(abs(Fraction(t)) for t in T)
            assert err <= bound


def test_three_folds_usually_correctly_rounded():
    rng = random.Random(15)
    hits = 0
    for trial in range(200):
        xs = data(rng, 100, 6)
        hits += reproducible_sum(xs) == math.fsum(xs)
    assert hits >= 190


def test_tiny_inputs_reach_the_bottom_level():
    rng = random.Random(16)
    for trial in range(20):
        xs = [rng.randint(-2 ** 40, 2 ** 40) * 5e-324 for _ in range(rng.randint(1, 300))]
        Ms = boundaries(max(abs(x) for x in xs) or 5e-324, len(xs), 3)
        assert Ms[-1] == 0.0
        assert reproducible_sum(xs) == math.fsum(xs)


def test_special_values():
    assert reproducible_sum([]) == 0.0
    assert reproducible_sum([0.0, -0.0]) == 0.0
    assert reproducible_sum([1.0, math.inf]) == math.inf
    assert math.isnan(reproducible_sum([math.inf, -math.inf, 1.0]))
    assert math.isnan(reproducible_sum([1.0, math.nan]))
    assert reproducible_sum([5e-324, 5e-324]) == 1e-323


def test_overflow_guard():
    try:
        reproducible_sum([1e308, 1e308])
    except OverflowError:
        pass
    else:
        raise AssertionError("expected OverflowError")
