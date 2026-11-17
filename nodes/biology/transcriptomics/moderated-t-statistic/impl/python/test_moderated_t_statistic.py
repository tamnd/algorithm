# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moderated-t-statistic/. The authors are listed in prov/SC6381.jsonl.

import math
import random
from fractions import Fraction

import pytest

from moderated_t_statistic import (
    betainc,
    digamma,
    fit_f_dist,
    moderated_t,
    ordinary_t,
    squeeze_var,
    t_sf,
    tetragamma,
    trigamma,
    trigamma_inverse,
)

EULER = 0.5772156649015329


def test_special_values():
    assert math.isclose(digamma(1.0), -EULER, rel_tol=1e-13)
    assert math.isclose(digamma(0.5), -EULER - 2 * math.log(2), rel_tol=1e-13)
    assert math.isclose(trigamma(1.0), math.pi ** 2 / 6, rel_tol=1e-13)
    assert math.isclose(trigamma(0.5), math.pi ** 2 / 2, rel_tol=1e-13)
    assert math.isclose(tetragamma(1.0), -2.4041138063191885, rel_tol=1e-12)
    for x in (0.3, 1.7, 3.7, 12.5, 200.0):
        assert math.isclose(digamma(x + 1) - digamma(x), 1 / x, rel_tol=1e-12)
        h = 1e-5 * x
        assert math.isclose((digamma(x + h) - digamma(x - h)) / (2 * h), trigamma(x), rel_tol=1e-6)
        assert math.isclose((trigamma(x + h) - trigamma(x - h)) / (2 * h), tetragamma(x), rel_tol=1e-5)


def test_trigamma_inverse_round_trip():
    for x in (0.01, 0.2, 1.0, 2.5, 10.0, 100.0, 1e4):
        assert math.isclose(trigamma_inverse(trigamma(x)), x, rel_tol=1e-8)
    with pytest.raises(ValueError):
        trigamma_inverse(0.0)


def test_betainc_against_the_binomial_sum():
    rng = random.Random(41)
    for _ in range(200):
        a = rng.randint(1, 12)
        b = rng.randint(1, 12)
        x = Fraction(rng.randint(1, 99), 100)
        n = a + b - 1
        exact = sum(math.comb(n, j) * x ** j * (1 - x) ** (n - j) for j in range(a, n + 1))
        assert math.isclose(betainc(a, b, float(x)), float(exact), rel_tol=1e-11, abs_tol=1e-15)


def test_t_tail_closed_forms():
    for t in (-3.0, -0.5, 0.0, 0.7, 2.0, 10.0, 100.0):
        assert math.isclose(t_sf(t, 1), 0.5 - math.atan(t) / math.pi, rel_tol=1e-11, abs_tol=1e-15)
        assert math.isclose(t_sf(t, 2), 0.5 - t / (2 * math.sqrt(2 + t * t)), rel_tol=1e-11, abs_tol=1e-15)
    assert math.isclose(t_sf(1.96, 1e9), t_sf(1.96, math.inf), rel_tol=1e-6)
    assert t_sf(0.0, 7.5) == 0.5


def test_d0_zero_gives_the_ordinary_t_and_infinite_d0_a_fixed_variance():
    rng = random.Random(42)
    a = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(20)]
    b = [[rng.gauss(0.5, 1) for _ in range(4)] for _ in range(20)]
    ts, ps, _, _ = moderated_t(a, b, prior=(0.0, 1.0))
    for g in range(20):
        t, p = ordinary_t(a[g], b[g])
        assert math.isclose(ts[g], t, rel_tol=1e-12)
        assert math.isclose(ps[g], p, rel_tol=1e-10)
    ts, ps, _, _ = moderated_t(a, b, prior=(math.inf, 2.0))
    for g in range(20):
        diff = sum(a[g]) / 3 - sum(b[g]) / 4
        assert math.isclose(ts[g], diff / math.sqrt(2.0 * (1 / 3 + 1 / 4)), rel_tol=1e-12)


def test_posterior_variance_lies_between_gene_and_prior():
    rng = random.Random(43)
    for _ in range(100):
        s2, s02 = rng.uniform(0.01, 5), rng.uniform(0.01, 5)
        post = squeeze_var(s2, 4, rng.uniform(0, 50), s02)
        assert min(s2, s02) - 1e-12 <= post <= max(s2, s02) + 1e-12


def test_equal_variances_give_infinite_prior_df():
    d0, s02 = fit_f_dist([0.3] * 10, 4)
    assert math.isinf(d0) and math.isclose(s02, 0.3)


def simulate(rng, genes, d0, s02, na=3, nb=3):
    a, b = [], []
    for _ in range(genes):
        sigma2 = d0 * s02 / rng.gammavariate(d0 / 2, 2)
        sd = math.sqrt(sigma2)
        a.append([rng.gauss(0, sd) for _ in range(na)])
        b.append([rng.gauss(0, sd) for _ in range(nb)])
    return a, b


def test_null_moderated_t_has_t_distribution_with_d0_plus_d_df():
    # The theorem: with the true prior, P(p <= u) = u. Checked at three levels
    # with the binomial tolerance 4 sqrt(u (1 - u) / G).
    rng = random.Random(44)
    genes = 4000
    a, b = simulate(rng, genes, 4.0, 1.0)
    _, ps, _, _ = moderated_t(a, b, prior=(4.0, 1.0))
    for u in (0.01, 0.05, 0.5):
        frac = sum(p <= u for p in ps) / genes
        assert abs(frac - u) <= 4 * math.sqrt(u * (1 - u) / genes)


def test_fit_f_dist_measurement():
    # A measurement: with 4000 genes, d = 4, d0 = 4 and s0^2 = 1, the moment
    # estimates come within these loose bounds.
    rng = random.Random(45)
    a, b = simulate(rng, 4000, 4.0, 1.0)
    _, _, d0, s02 = moderated_t(a, b)
    assert 2.5 < d0 < 7.0
    assert abs(s02 - 1.0) < 0.15


def test_errors():
    with pytest.raises(ValueError):
        moderated_t([[1.0, 2.0]], [[3.0, 4.0], [1.0]])
    with pytest.raises(ValueError):
        fit_f_dist([1.0], 3)
    with pytest.raises(ValueError):
        digamma(0.0)
