# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-response/. The authors are listed in prov/935KM5.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

import dpkit
from randomized_response import (
    estimate_fraction,
    estimate_variance,
    randomized_response,
    report_pmf,
    truth_probability,
)

BITS = (0, 1)


def one_bit_pmf(x):
    return report_pmf(x[0], 3)


def vector_pmf(x, exp_epsilon):
    """Exact pmf of the vector of reports, one independent coin per record."""
    out = {}
    for y in itertools.product(BITS, repeat=len(x)):
        pr = Fraction(1)
        for v, r in zip(x, y):
            pr *= report_pmf(v, exp_epsilon)[r]
        out[y] = pr
    return out


def test_check_values():
    assert truth_probability(3) == Fraction(3, 4)
    assert abs(float(truth_probability(Fraction(math.exp(1)))) - 0.731059) < 5e-7
    assert truth_probability(1) == Fraction(1, 2)


def test_two_coin_version_equals_exp_epsilon_three():
    # Dwork and Roth: flip a coin; on tails answer truthfully, on heads answer with a second coin.
    for v in BITS:
        two_coin = {v: Fraction(1, 2) + Fraction(1, 4), 1 - v: Fraction(1, 4)}
        assert report_pmf(v, 3) == two_coin


def test_one_bit_is_exactly_ln3_dp():
    pairs = [((0,), (1,))]
    assert dpkit.is_pure_dp(one_bit_pmf, pairs, math.log(3))
    assert not dpkit.is_pure_dp(one_bit_pmf, pairs, math.log(3) - 0.01)
    p, q = one_bit_pmf((0,)), one_bit_pmf((1,))
    assert abs(dpkit.max_privacy_loss(p, q) - math.log(3)) < 1e-15


def test_privacy_loss_equals_epsilon_for_random_rationals():
    rng = random.Random(3)
    for _ in range(500):
        e = Fraction(rng.randint(10, 200), 10)
        p, q = report_pmf(0, e), report_pmf(1, e)
        assert p[0] / q[0] == e
        assert q[1] / p[1] == e
        assert abs(dpkit.max_privacy_loss(p, q) - math.log(e)) < 1e-12


def test_vector_of_reports_under_replace_neighbors():
    # Each person randomizes alone, so a change of one bit costs epsilon.
    e = Fraction(5, 2)
    for n in range(1, 5):
        for x in itertools.product(BITS, repeat=n):
            pairs = [(x, y) for y in dpkit.neighbors_replace(x, BITS)]
            mech = lambda d: vector_pmf(d, e)
            assert dpkit.is_pure_dp(mech, pairs, math.log(e))
            assert not dpkit.is_pure_dp(mech, pairs, math.log(e) - 0.01)


def test_estimate_is_unbiased_and_variance_matches_exactly():
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(1, 6)
        x = tuple(rng.choice(BITS) for _ in range(n))
        e = Fraction(rng.randint(11, 60), 10)
        pmf = vector_pmf(x, e)
        assert sum(pmf.values()) == 1
        mean = sum(pr * estimate_fraction(y, e) for y, pr in pmf.items())
        assert mean == Fraction(sum(x), n)
        var = sum(pr * (estimate_fraction(y, e) - mean) ** 2 for y, pr in pmf.items())
        assert var == estimate_variance(n, e)


def test_sampler_matches_pmf():
    rng = random.Random(2024)
    n = 2000
    t = dpkit.hoeffding_margin(n, 1e-6)
    for e in (Fraction(1), Fraction(3), Fraction(27, 10), Fraction(19)):
        for v in BITS:
            reports = [randomized_response(v, e, rng) for _ in range(n)]
            freq = dpkit.empirical_pmf(reports).get(v, 0.0)
            assert abs(freq - float(truth_probability(e))) <= t


def test_estimate_of_population_is_accurate():
    rng = random.Random(99)
    n = 2000
    beta = 1e-6
    for e in (Fraction(3), Fraction(7)):
        x = [1 if rng.random() < 0.3 else 0 for _ in range(n)]
        reports = [randomized_response(v, e, rng) for v in x]
        p = truth_probability(e)
        # lambda is a mean of n independent bits, so Hoeffding applies to it.
        bound = dpkit.hoeffding_margin(n, beta) / float(2 * p - 1)
        assert abs(float(estimate_fraction(reports, e)) - sum(x) / n) <= bound


def test_edge_cases():
    rng = random.Random(0)
    with pytest.raises(ValueError):
        randomized_response(2, 3, rng)
    with pytest.raises(ValueError):
        truth_probability(Fraction(1, 2))
    with pytest.raises(ValueError):
        estimate_fraction([], 3)
    with pytest.raises(ValueError):
        estimate_fraction([0, 1], 1)
    # The estimate can leave [0, 1]; that is the price of unbiasedness.
    assert estimate_fraction([0, 0, 0], 3) == Fraction(-1, 2)
    assert estimate_fraction([1, 1, 1], 3) == Fraction(3, 2)
