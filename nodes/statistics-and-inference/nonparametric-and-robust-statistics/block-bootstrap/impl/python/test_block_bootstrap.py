# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-bootstrap/. The authors are listed in prov/Q86QP6.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from block_bootstrap import (
    block_bootstrap,
    circular_block_resample,
    mbb_mean_moments,
    moving_block_resample,
    standard_deviation,
    stationary_mean_variance,
    stationary_resample,
)


def fr_mean(xs):
    return sum(xs, Fraction(0)) / len(xs)


def law_moments(outcomes):
    """Mean and variance of a finite law given as (value, probability) pairs."""
    m = sum(p * v for v, p in outcomes)
    return m, sum(p * (v - m) ** 2 for v, p in outcomes)


def random_series(rng, n):
    return [Fraction(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(n)]


def test_moving_block_variance_matches_all_block_choices():
    rng = random.Random(1)
    for n, l in ((6, 1), (6, 2), (6, 3), (8, 2), (8, 4), (9, 3)):
        x = random_series(rng, n)
        k, big_n = n // l, n - l + 1
        w = Fraction(1, big_n**k)
        outcomes = []
        for starts in itertools.product(range(big_n), repeat=k):
            xs = [x[s + t] for s in starts for t in range(l)]
            outcomes.append((fr_mean(xs), w))
        assert law_moments(outcomes) == mbb_mean_moments(x, l)


def test_block_length_one_is_the_iid_bootstrap():
    x = [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0]
    a = moving_block_resample(x, 1, random.Random(7))
    g = random.Random(7)
    assert a == [x[g.randrange(8)] for _ in range(8)]
    xf = [Fraction(v) for v in x]
    m = fr_mean(xf)
    assert mbb_mean_moments(xf, 1) == (m, sum((v - m) ** 2 for v in xf) / 64)


def test_moving_blocks_underweight_the_ends():
    x = [Fraction(v) for v in (10, 0, 0, 0, 0, 0)]
    centre, _ = mbb_mean_moments(x, 2)
    assert centre == Fraction(1, 1) and fr_mean(x) == Fraction(5, 3)


def test_circular_block_bootstrap_is_centred_exactly():
    rng = random.Random(2)
    n, l = 6, 2
    x = random_series(rng, n)
    k = n // l
    outcomes = []
    for starts in itertools.product(range(n), repeat=k):
        xs = [x[(s + t) % n] for s in starts for t in range(l)]
        outcomes.append((fr_mean(xs), Fraction(1, n**k)))
    assert law_moments(outcomes)[0] == fr_mean(x)


def stationary_law(x, p):
    """The exact law of the stationary bootstrap mean, by listing all n^n index paths."""
    n = len(x)
    outcomes = []
    for path in itertools.product(range(n), repeat=n):
        prob = Fraction(1, n)
        for a, b in zip(path, path[1:]):
            prob *= p / n + (1 - p) * (b == (a + 1) % n)
        if prob:
            outcomes.append((fr_mean([x[i] for i in path]), prob))
    return outcomes


def test_stationary_bootstrap_mean_and_variance_exact():
    rng = random.Random(3)
    for n, p in ((3, Fraction(1, 2)), (4, Fraction(1, 3)), (5, Fraction(1, 4)), (5, Fraction(1))):
        x = random_series(rng, n)
        law = stationary_law(x, p)
        assert sum(q for _, q in law) == 1
        mean, var = law_moments(law)
        assert mean == fr_mean(x)
        assert var == stationary_mean_variance(x, p)


def test_resample_shapes():
    rng = random.Random(4)
    x = list(range(20))
    for _ in range(50):
        xs = moving_block_resample(x, 6, rng)
        assert len(xs) == 20
        for j in range(0, 18, 6):
            assert xs[j : j + 6] == list(range(xs[j], xs[j] + 6))
        assert len(circular_block_resample(x, 6, rng)) == 20
        assert len(stationary_resample(x, 0.2, rng)) == 20
    with pytest.raises(ValueError):
        moving_block_resample(x, 0, rng)
    with pytest.raises(ValueError):
        stationary_resample(x, 0.0, rng)


def test_monte_carlo_matches_the_exact_variance():
    rng = random.Random(5)
    x = [rng.gauss(0.0, 1.0) for _ in range(24)]
    reps = block_bootstrap(x, lambda v: math.fsum(v) / len(v), 4000, random.Random(6), l=4)
    _, exact = mbb_mean_moments(x, 4)
    assert abs(standard_deviation(reps) ** 2 / exact - 1) < 0.1


def ar1(rng, n, phi):
    x = [rng.gauss(0.0, 1.0) / math.sqrt(1 - phi * phi)]
    for _ in range(n - 1):
        x.append(phi * x[-1] + rng.gauss(0.0, 1.0))
    return x


def ar1_mean_variance(n, phi):
    g = [phi**h / (1 - phi * phi) for h in range(n)]
    return (g[0] + 2 * sum((1 - h / n) * g[h] for h in range(1, n))) / n


def test_dependence_measured_on_ar1():
    """Measured, not proved: for AR(1) with phi = 0.5 the iid bootstrap variance of the mean is
    about (1 - phi)/(1 + phi) = 1/3 of the truth; blocks of length near n^(1/3) recover most of it."""
    rng = random.Random(8)
    n, phi, r = 125, 0.5, 300
    truth = ar1_mean_variance(n, phi)
    iid, mbb, sb = [], [], []
    for _ in range(r):
        x = ar1(rng, n, phi)
        m = math.fsum(x) / n
        iid.append(math.fsum((v - m) ** 2 for v in x) / n / n / truth)
        mbb.append(mbb_mean_moments(x[:120], 5)[1] / ar1_mean_variance(120, phi))
        sb.append(stationary_mean_variance(x, 0.2) / truth)
    assert abs(math.fsum(iid) / r - 1 / 3) < 0.06
    assert math.fsum(mbb) / r > 0.65
    assert math.fsum(sb) / r > 0.65
