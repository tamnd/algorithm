# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-mechanism/. The authors are listed in prov/12JV5Q.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

import dpkit
from geometric_mechanism import geometric_mechanism, noise_pmf, noise_tail, truncated_pmf

UNIVERSE = (0, 1)


def count_ones(x):
    return sum(x)


def all_datasets(max_n):
    for n in range(max_n + 1):
        for x in itertools.combinations_with_replacement(UNIVERSE, n):
            yield x


def convolution_pmf(d, alpha, terms=400):
    """P(G1 - G2 = d) by a direct sum over G2 = k, with G1 = k + d. Float oracle."""
    a = float(alpha)
    total = 0.0
    for k in range(terms):
        j = k + d
        if j >= 0:
            total += (1 - a) * a ** j * (1 - a) * a ** k
    return total


def test_check_values():
    alpha = Fraction(1, 2)  # epsilon = ln 2
    assert noise_pmf(0, alpha) == Fraction(1, 3)
    assert noise_pmf(1, alpha) == Fraction(1, 6)
    assert noise_pmf(-2, alpha) == Fraction(1, 12)
    assert noise_tail(1, alpha) == Fraction(2, 3)
    assert abs(math.log(1 / alpha) - math.log(2)) < 1e-15


def test_closed_form_matches_convolution():
    rng = random.Random(5)
    for _ in range(500):
        alpha = Fraction(rng.randint(1, 9), 10)
        d = rng.randint(-8, 8)
        assert abs(float(noise_pmf(d, alpha)) - convolution_pmf(d, alpha)) < 1e-12


def test_noise_pmf_and_tail_are_consistent():
    rng = random.Random(6)
    for _ in range(500):
        alpha = Fraction(rng.randint(1, 30), 31)
        t = rng.randint(1, 10)
        inside = sum(noise_pmf(d, alpha) for d in range(-(t - 1), t))
        assert inside + noise_tail(t, alpha) == 1


def test_truncated_pmf_matches_clamp_of_noise():
    rng = random.Random(8)
    for _ in range(500):
        alpha = Fraction(rng.randint(1, 9), 10)
        lo = rng.randint(-3, 3)
        hi = lo + rng.randint(0, 6)
        v = rng.randint(lo, hi)
        got = truncated_pmf(v, alpha, lo, hi)
        assert sum(got.values()) == 1
        # Oracle: clamp the untruncated noise; the tails are geometric series.
        want = {}
        for z in range(lo, hi + 1):
            want[z] = noise_pmf(z - v, alpha)
        if lo < hi:
            a = alpha
            want[lo] += (1 - a) / (1 + a) * a ** (v - lo + 1) / (1 - a)
            want[hi] += (1 - a) / (1 + a) * a ** (hi - v + 1) / (1 - a)
        else:
            want = {lo: Fraction(1)}
        assert got == want


def test_counting_query_is_exactly_ln_inverse_alpha_dp():
    for alpha in (Fraction(1, 2), Fraction(1, 3), Fraction(4, 5)):
        eps = math.log(1 / alpha)
        lo, hi = 0, 6
        mech = lambda x: truncated_pmf(count_ones(x), alpha, lo, hi)
        add_remove = [(x, y) for x in all_datasets(5) for y in dpkit.neighbors_add_remove(x, UNIVERSE)]
        replace = [(x, y) for x in all_datasets(5) for y in dpkit.neighbors_replace(x, UNIVERSE)]
        for pairs in (add_remove, replace):
            assert dpkit.is_pure_dp(mech, pairs, eps)
            assert not dpkit.is_pure_dp(mech, pairs, eps - 0.01)


def test_sensitivity_two_needs_square_root_of_alpha():
    # A query of sensitivity 2 with alpha = 1/4 costs 2 ln 4 = ln 16, not ln 4.
    lo, hi = -2, 12
    double = lambda x: truncated_pmf(2 * count_ones(x), Fraction(1, 4), lo, hi)
    pairs = [(x, y) for x in all_datasets(5) for y in dpkit.neighbors_add_remove(x, UNIVERSE)]
    assert dpkit.is_pure_dp(double, pairs, math.log(16))
    assert not dpkit.is_pure_dp(double, pairs, math.log(4))


def test_sampler_matches_pmf():
    rng = random.Random(77)
    n = 2000
    beta = 1e-6
    for alpha in (Fraction(1, 2), Fraction(9, 10)):
        x = (1, 0, 1, 1)
        samples = [geometric_mechanism(x, count_ones, alpha, rng) for _ in range(n)]
        emp = dpkit.empirical_pmf(samples)
        t = dpkit.hoeffding_margin(n, beta / 41)
        for z in range(3 - 20, 3 + 21):
            assert abs(emp.get(z, 0.0) - float(noise_pmf(z - 3, alpha))) <= t
        clamped = [geometric_mechanism(x, count_ones, alpha, rng, 0, 4) for _ in range(n)]
        emp = dpkit.empirical_pmf(clamped)
        want = truncated_pmf(3, alpha, 0, 4)
        t = dpkit.hoeffding_margin(n, beta / 5)
        assert set(emp) <= set(want)
        for z, pr in want.items():
            assert abs(emp.get(z, 0.0) - float(pr)) <= t


def test_mean_absolute_error_matches_closed_form():
    # E|Z| = 2 alpha / (1 - alpha^2), from the sum over d of |d| P(Z = d).
    for alpha in (Fraction(1, 2), Fraction(2, 3)):
        partial = sum(abs(d) * noise_pmf(d, alpha) for d in range(-200, 201))
        assert abs(float(partial) - float(2 * alpha / (1 - alpha ** 2))) < 1e-12


def test_edge_cases():
    rng = random.Random(1)
    with pytest.raises(ValueError):
        geometric_mechanism((), count_ones, 1, rng)
    with pytest.raises(ValueError):
        geometric_mechanism((), count_ones, 0, rng)
    with pytest.raises(ValueError):
        geometric_mechanism((), count_ones, Fraction(1, 2), rng, 3, 2)
    with pytest.raises(ValueError):
        truncated_pmf(5, Fraction(1, 2), 0, 4)
    with pytest.raises(ValueError):
        noise_tail(0, Fraction(1, 2))
    assert truncated_pmf(0, Fraction(1, 2), 0, 0) == {0: 1}
    assert geometric_mechanism((), count_ones, Fraction(1, 2), rng, 0, 0) == 0
    assert all(0 <= geometric_mechanism((1, 1), count_ones, Fraction(1, 2), rng, 0, 2) <= 2 for _ in range(200))
