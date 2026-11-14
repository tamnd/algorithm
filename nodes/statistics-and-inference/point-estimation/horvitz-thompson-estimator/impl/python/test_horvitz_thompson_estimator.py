# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horvitz-thompson-estimator/. The authors are listed in prov/D95ZRB.jsonl.

import itertools
import random
from fractions import Fraction

from horvitz_thompson_estimator import hajek_mean, ht_interval, ht_total, ht_variance, syg_variance
from stdist import norm_ppf


def inclusion(design, units):
    """pi_i and pi_ij of a design given as {sample tuple: probability}, by summing."""
    pi = {i: sum((p for s, p in design.items() if i in s), Fraction(0)) for i in units}
    pij = {(i, j): sum((p for s, p in design.items() if i in s and j in s), Fraction(0))
           for i in units for j in units}
    return pi, pij


def moments(design, values):
    """Mean and variance over the design of the given per-sample values."""
    mean = sum((p * values[s] for s, p in design.items()), Fraction(0))
    var = sum((p * (values[s] - mean) ** 2 for s, p in design.items()), Fraction(0))
    return mean, var


def var_formula(y, pi, pij, units):
    return sum(((pij[i, j] - pi[i] * pi[j]) * y[i] / pi[i] * y[j] / pi[j]
                for i in units for j in units), Fraction(0))


def random_fixed_design(rng, n_units, size):
    """Every subset of the given size gets a positive random probability."""
    subsets = list(itertools.combinations(range(n_units), size))
    w = [rng.randint(1, 9) for _ in subsets]
    total = sum(w)
    return {s: Fraction(wi, total) for s, wi in zip(subsets, w)}


EXAMPLE = {(1, 2): Fraction(1, 10), (1, 3): Fraction(1, 10), (1, 4): Fraction(2, 10),
           (2, 3): Fraction(1, 10), (2, 4): Fraction(2, 10), (3, 4): Fraction(3, 10)}
EXAMPLE_Y = {1: 2, 2: 3, 3: 6, 4: 10}


def test_running_example_table():
    units = [1, 2, 3, 4]
    pi, pij = inclusion(EXAMPLE, units)
    assert [pi[i] for i in units] == [Fraction(2, 5), Fraction(2, 5), Fraction(1, 2), Fraction(7, 10)]
    q = lambda i, j: pij[i, j]
    y = EXAMPLE_Y
    expected = {
        (1, 2): (Fraction(25, 2), Fraction(15, 4), Fraction(15, 4), Fraction(5, 2)),
        (1, 3): (Fraction(17), Fraction(-33), Fraction(49), Fraction(34, 9)),
        (1, 4): (Fraction(135, 7), Fraction(935, 49), Fraction(1690, 49), Fraction(54, 11)),
        (2, 3): (Fraction(39, 2), Fraction(-297, 4), Fraction(81, 4), Fraction(13, 3)),
        (2, 4): (Fraction(305, 14), Fraction(1815, 196), Fraction(1805, 98), Fraction(61, 11)),
        (3, 4): (Fraction(184, 7), Fraction(3728, 49), Fraction(128, 147), Fraction(23, 3)),
    }
    for s, row in expected.items():
        got = (ht_total(s, y, pi), ht_variance(s, y, pi, q), syg_variance(s, y, pi, q), hajek_mean(s, y, pi))
        assert got == row
    est = {s: ht_total(s, y, pi) for s in EXAMPLE}
    mean, var = moments(EXAMPLE, est)
    assert mean == 21 and var == Fraction(127, 7) == var_formula(y, pi, pij, units)
    assert moments(EXAMPLE, {s: ht_variance(s, y, pi, q) for s in EXAMPLE})[0] == Fraction(127, 7)
    assert moments(EXAMPLE, {s: syg_variance(s, y, pi, q) for s in EXAMPLE})[0] == Fraction(127, 7)
    assert moments(EXAMPLE, {s: hajek_mean(s, y, pi) for s in EXAMPLE})[0] == Fraction(2159, 396)


def test_unbiased_by_enumeration_fixed_size():
    rng = random.Random(1952)
    for _ in range(150):
        n_units = rng.randint(3, 6)
        size = rng.randint(2, n_units - 1)
        design = random_fixed_design(rng, n_units, size)
        units = list(range(n_units))
        y = [Fraction(rng.randint(-20, 30), rng.randint(1, 4)) for _ in units]
        pi, pij = inclusion(design, units)
        q = lambda i, j: pij[i, j]
        assert sum(pi.values()) == size
        est = {s: ht_total(s, y, pi) for s in design}
        mean, var = moments(design, est)
        assert mean == sum(y)
        assert var == var_formula(y, pi, pij, units)
        syg_form = sum(((pi[i] * pi[j] - pij[i, j]) * (y[i] / pi[i] - y[j] / pi[j]) ** 2
                        for i, j in itertools.combinations(units, 2)), Fraction(0))
        assert var == syg_form
        assert moments(design, {s: ht_variance(s, y, pi, q) for s in design})[0] == var
        assert moments(design, {s: syg_variance(s, y, pi, q) for s in design})[0] == var


def test_unbiased_by_enumeration_poisson_sampling():
    rng = random.Random(7)
    for _ in range(40):
        n_units = rng.randint(1, 6)
        units = list(range(n_units))
        pi = [Fraction(rng.randint(1, 9), 10) for _ in units]
        y = [Fraction(rng.randint(-15, 15)) for _ in units]
        design = {}
        for bits in itertools.product((0, 1), repeat=n_units):
            s = tuple(i for i in units if bits[i])
            p = Fraction(1)
            for i in units:
                p *= pi[i] if bits[i] else 1 - pi[i]
            design[s] = p
        q = lambda i, j: pi[i] * pi[j]
        est = {s: ht_total(s, y, pi) for s in design}
        mean, var = moments(design, est)
        assert mean == sum(y)
        assert var == sum(((1 - pi[i]) * y[i] ** 2 / pi[i] for i in units), Fraction(0))
        assert moments(design, {s: ht_variance(s, y, pi, q) for s in design})[0] == var


def test_simple_random_sampling_closed_forms():
    rng = random.Random(3)
    for _ in range(100):
        big_n = rng.randint(3, 7)
        n = rng.randint(2, big_n)
        y = [Fraction(rng.randint(-10, 40)) for _ in range(big_n)]
        f = Fraction(n, big_n)
        pi = [f] * big_n
        q = lambda i, j: Fraction(n * (n - 1), big_n * (big_n - 1))
        samples = list(itertools.combinations(range(big_n), n))
        for s in samples:
            ys = [y[i] for i in s]
            ybar = sum(ys, Fraction(0)) / n
            s2 = sum(((v - ybar) ** 2 for v in ys), Fraction(0)) / (n - 1)
            closed = big_n ** 2 * (1 - f) * s2 / n
            assert ht_total(s, y, pi) == big_n * ybar
            assert ht_variance(s, y, pi, q) == closed == syg_variance(s, y, pi, q)
        mean_y = sum(y, Fraction(0)) / big_n
        pop_s2 = sum(((v - mean_y) ** 2 for v in y), Fraction(0)) / (big_n - 1)
        uniform = {s: Fraction(1, len(samples)) for s in samples}
        mean, var = moments(uniform, {s: ht_total(s, y, pi) for s in samples})
        assert mean == sum(y) and var == big_n ** 2 * (1 - f) * pop_s2 / n


def test_proportion_can_exceed_one_and_hajek_stays_in_range():
    pi, _ = inclusion(EXAMPLE, [1, 2, 3, 4])
    yb = {1: 1, 2: 1, 3: 0, 4: 1}
    assert ht_total((1, 2), yb, pi) / 4 == Fraction(5, 4)
    assert hajek_mean((1, 2), yb, pi) == 1
    est = {s: ht_total(s, yb, pi) / 4 for s in EXAMPLE}
    assert moments(EXAMPLE, est)[0] == Fraction(3, 4)


def test_zero_probabilities_are_rejected():
    for bad in (lambda: ht_total([0, 1], [1, 2], [Fraction(1, 2), 0]),
                lambda: ht_variance([0, 1], [1, 2], [Fraction(1, 2)] * 2, lambda i, j: 0),
                lambda: syg_variance([0, 1], [1, 2], [Fraction(1, 2)] * 2, lambda i, j: 0),
                lambda: ht_total([0, 0], [1, 2], [Fraction(1, 2)] * 2),
                lambda: ht_interval(10.0, -1.0)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")


def test_missing_units_bias():
    # Unit 2 is never sampled: the expectation misses exactly its value.
    design = {(0,): Fraction(1, 2), (1,): Fraction(1, 2)}
    y = [Fraction(4), Fraction(6), Fraction(5)]
    pi = [Fraction(1, 2), Fraction(1, 2), Fraction(0)]
    mean, _ = moments(design, {s: ht_total(s, y, pi) for s in design})
    assert mean == sum(y) - y[2]


def test_normal_interval_coverage_simple_random_sampling():
    # Measured, not proved: about 95 percent coverage for n = 30 of N = 120.
    rng = random.Random(2024)
    big_n, n, reps = 120, 30, 1000
    y = [rng.gammavariate(4.0, 5.0) for _ in range(big_n)]
    total = sum(y)
    f = n / big_n
    pi = [f] * big_n
    joint = n * (n - 1) / (big_n * (big_n - 1))
    q = lambda i, j: joint
    lo, hi = ht_interval(0.0, 1.0, 0.95)
    assert abs(hi - norm_ppf(0.975)) < 1e-15 and lo == -hi
    covered = 0
    for _ in range(reps):
        s = rng.sample(range(big_n), n)
        a, b = ht_interval(ht_total(s, y, pi), syg_variance(s, y, pi, q))
        covered += a <= total <= b
    assert 0.92 <= covered / reps <= 0.97
