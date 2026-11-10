# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-moving-average/. The authors are listed in prov/G9PD69.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from exponential_moving_average import (
    alpha_from_com,
    alpha_from_halflife,
    alpha_from_span,
    ema,
    ema_corrected,
    weighted_mean_form,
)


def test_page_example():
    xs = [4, 8, 6, 2]
    a = F(1, 2)
    assert list(ema(xs, a, start="zero")) == [2, 5, F(11, 2), F(15, 4)]
    assert list(ema(xs, a, start="first")) == [4, 6, 6, 4]
    assert list(ema_corrected(xs, a)) == [4, F(20, 3), F(44, 7), 4]


def rand_fracs(rng, n):
    return [F(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(n)]


def test_weights_identity_exact():
    rng = random.Random(1)
    for _ in range(60):
        a = F(rng.randint(1, 9), 10)
        xs = rand_fracs(rng, rng.randint(1, 25))
        t = len(xs)
        # start "zero": s_t = alpha * sum (1 - alpha)^j x_{t-j}
        want = a * sum((1 - a) ** j * xs[t - 1 - j] for j in range(t))
        assert list(ema(xs, a, start="zero"))[-1] == want
        # start "first": the oldest item keeps the weight (1 - alpha)^(t-1)
        want1 = sum(a * (1 - a) ** j * xs[t - 1 - j] for j in range(t - 1)) + (1 - a) ** (t - 1) * xs[0]
        assert list(ema(xs, a, start="first"))[-1] == want1
        # the weights of start "first" sum to 1
        assert sum(a * (1 - a) ** j for j in range(t - 1)) + (1 - a) ** (t - 1) == 1


def test_bias_correction_is_normalized_weighted_mean():
    rng = random.Random(2)
    for _ in range(60):
        a = F(rng.randint(1, 19), 20)
        xs = rand_fracs(rng, rng.randint(1, 20))
        got = list(ema_corrected(xs, a))
        for t in range(1, len(xs) + 1):
            assert got[t - 1] == weighted_mean_form(xs[:t], a)
        # a constant stream gives the constant at every step
        c = F(7, 3)
        assert all(v == c for v in ema_corrected([c] * 10, a))


def test_span_matches_mean_age_and_noise_variance():
    for n in range(1, 40):
        a = alpha_from_span(F(n))
        mean_age_ema = (1 - a) / a  # sum j a (1-a)^j
        mean_age_sma = F(n - 1, 2)
        assert mean_age_ema == mean_age_sma
        # variance factor of white noise: sum a^2 (1-a)^(2j) = a / (2 - a) = 1/N
        assert a / (2 - a) == F(1, n)
        assert alpha_from_com(mean_age_ema) == a
    # partial sums agree with the closed forms (truncated series, exact rationals)
    a = F(1, 4)
    terms = 200
    s_age = sum(j * a * (1 - a) ** j for j in range(terms))
    s_var = sum(a * a * (1 - a) ** (2 * j) for j in range(terms))
    assert abs(s_age - (1 - a) / a) < F(1, 10 ** 20)
    assert abs(s_var - a / (2 - a)) < F(1, 10 ** 20)


def test_weight_in_last_n_items_tends_to_one_minus_e_minus_2():
    for n in [1, 2, 5, 20, 1000]:
        a = 2 / (n + 1)
        share = 1 - (1 - a) ** n
        assert share >= 1 - math.exp(-2) - 1e-12
    n = 10 ** 6
    assert abs(1 - (1 - 2 / (n + 1)) ** n - (1 - math.exp(-2))) < 1e-6


def test_halflife():
    for h in [0.5, 1, 3, 10, 100]:
        a = alpha_from_halflife(h)
        assert abs((1 - a) ** h - 0.5) < 1e-12


def test_float_against_fraction():
    rng = random.Random(5)
    xs = [rng.uniform(-1, 1) for _ in range(300)]
    a = 0.125  # exact in binary, so only the additions round
    exact = list(ema([F(x) for x in xs], F(a), start="first"))
    for got, want in zip(ema(xs, a), exact):
        assert abs(got - float(want)) < 1e-14


def test_bad_alpha():
    with pytest.raises(ValueError):
        list(ema([1], 0))
    with pytest.raises(ValueError):
        list(ema([1], 1.5))
