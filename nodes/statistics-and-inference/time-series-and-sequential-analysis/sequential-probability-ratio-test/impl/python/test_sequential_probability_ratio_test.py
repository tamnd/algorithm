# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-probability-ratio-test/. The authors are listed in prov/9JY1HF.jsonl.
import itertools
import math
import random
from fractions import Fraction

import pytest

from sequential_probability_ratio_test import (
    bernoulli_sprt_exact,
    bernoulli_sprt_moments_exact,
    sprt,
    wald_asn,
    wald_thresholds,
)


def coin(p0: float, p1: float):
    return (lambda x: math.log(p0 if x else 1.0 - p0)), (lambda x: math.log(p1 if x else 1.0 - p1))


def test_worked_example():
    a, b = wald_thresholds(0.1, 0.1)
    assert abs(b - math.log(9.0)) < 1e-12 and abs(a + math.log(9.0)) < 1e-12
    lf0, lf1 = coin(0.5, 0.8)
    decision, n, lam = sprt([1, 1, 0, 1, 1, 1, 1, 1], lf0, lf1, 0.1, 0.1)
    assert (decision, n) == ("reject H0", 8)
    assert abs(lam - (7 * math.log(1.6) + math.log(0.4))) < 1e-12


def test_accept_and_no_decision():
    lf0, lf1 = coin(0.5, 0.8)
    assert sprt([0, 0, 0], lf0, lf1, 0.1, 0.1)[:2] == ("accept H0", 3)
    assert sprt([1, 0], lf0, lf1, 0.1, 0.1)[:2] == ("no decision", 2)
    assert sprt([], lf0, lf1, 0.1, 0.1)[:2] == ("no decision", 0)


def test_bad_thresholds():
    with pytest.raises(ValueError):
        wald_thresholds(0.6, 0.5)
    with pytest.raises(ValueError):
        wald_thresholds(0.0, 0.1)


def brute_force(p0: float, p1: float, p: float, alpha: float, beta: float, n: int) -> tuple[float, float]:
    """Run the SPRT on every 0-1 sequence of length n and add up the probabilities."""
    lf0, lf1 = coin(p0, p1)
    rej = acc = 0.0
    for seq in itertools.product((0, 1), repeat=n):
        w = math.prod(p if x else 1.0 - p for x in seq)
        d = sprt(seq, lf0, lf1, alpha, beta)[0]
        rej += w * (d == "reject H0")
        acc += w * (d == "accept H0")
    return rej, acc


def test_dynamic_program_matches_enumeration():
    for p0, p1, alpha, beta in ((0.5, 0.8, 0.1, 0.1), (0.3, 0.6, 0.05, 0.2), (0.6, 0.4, 0.1, 0.05)):
        for p in (p0, p1, 0.5):
            rej, acc, _, _ = bernoulli_sprt_exact(p0, p1, p, alpha, beta, 12)
            r2, a2 = brute_force(p0, p1, p, alpha, beta, 12)
            assert abs(rej - r2) < 1e-12 and abs(acc - a2) < 1e-12


@pytest.mark.parametrize("p0, p1, alpha, beta", [(0.5, 0.8, 0.1, 0.1), (0.3, 0.5, 0.05, 0.2),
                                                  (0.5, 0.6, 0.05, 0.05), (0.2, 0.1, 0.01, 0.1)])
def test_wald_error_bounds_exact(p0, p1, alpha, beta):
    rej0, acc0, _, left0 = bernoulli_sprt_exact(p0, p1, p0, alpha, beta, 3000)
    rej1, acc1, _, left1 = bernoulli_sprt_exact(p0, p1, p1, alpha, beta, 3000)
    assert left0 < 1e-12 and left1 < 1e-12
    a_err, b_err = rej0, acc1
    assert a_err <= alpha / (1.0 - beta)
    assert b_err <= beta / (1.0 - alpha)
    assert a_err + b_err <= alpha + beta
    # Ville: P0(Lambda ever reaches b) <= exp(-b) = alpha / (1 - beta) as well.
    assert a_err <= math.exp(-wald_thresholds(alpha, beta)[1]) + 1e-15


def test_worked_example_operating_characteristics():
    rej0, _, en0, _ = bernoulli_sprt_exact(0.5, 0.8, 0.5, 0.1, 0.1, 600)
    _, acc1, en1, _ = bernoulli_sprt_exact(0.5, 0.8, 0.8, 0.1, 0.1, 600)
    assert abs(rej0 - 0.08443) < 1e-5 and abs(acc1 - 0.07738) < 1e-5
    assert abs(en0 - 9.365) < 1e-3 and abs(en1 - 10.474) < 1e-3
    a, b = wald_thresholds(0.1, 0.1)
    ez0 = 0.5 * math.log(1.6) + 0.5 * math.log(0.4)
    ez1 = 0.8 * math.log(1.6) + 0.2 * math.log(0.4)
    assert abs(wald_asn(ez0, 0.1, a, b) - 7.877) < 1e-3
    assert abs(wald_asn(ez1, 0.9, a, b) - 9.120) < 1e-3


def test_walds_equation_exact():
    for p in (Fraction(1, 2), Fraction(4, 5), Fraction(2, 3)):
        for n_max in (5, 17, 30):
            e_h, e_t = bernoulli_sprt_moments_exact(0.5, 0.8, p, 0.1, 0.1, n_max)
            assert e_h == p * e_t


def test_normal_monte_carlo_against_wald_bounds():
    rng = random.Random(11)
    mu, alpha, beta = 0.5, 0.05, 0.05
    lf0 = lambda x: -0.5 * x * x  # noqa: E731
    lf1 = lambda x: -0.5 * (x - mu) ** 2  # noqa: E731
    reps = 4000
    for theta, bound in ((0.0, alpha / (1 - beta)), (mu, beta / (1 - alpha))):
        errors = 0
        total = 0

        def stream():
            while True:
                yield rng.gauss(theta, 1.0)

        for _ in range(reps):
            d, n, _ = sprt(stream(), lf0, lf1, alpha, beta)
            errors += d == ("reject H0" if theta == 0.0 else "accept H0")
            total += n
        se = math.sqrt(bound * (1 - bound) / reps)
        assert errors / reps < bound + 4 * se
        # The ASN sits above Wald's overshoot-free value 21.2 and far below the fixed sample size 43.3.
        assert 21.0 < total / reps < 28.0


def test_random_streams_against_direct_rule():
    rng = random.Random(2026)
    for _ in range(500):
        p0 = rng.uniform(0.1, 0.9)
        p1 = rng.uniform(0.1, 0.9)
        if abs(p0 - p1) < 0.05:
            continue
        alpha, beta = rng.uniform(0.01, 0.2), rng.uniform(0.01, 0.2)
        seq = [int(rng.random() < 0.5) for _ in range(rng.randint(0, 30))]
        lf0, lf1 = coin(p0, p1)
        a, b = math.log(beta / (1 - alpha)), math.log((1 - beta) / alpha)
        want = ("no decision", len(seq))
        lam = 0.0
        for i, x in enumerate(seq, 1):
            lam += math.log((p1 if x else 1 - p1) / (p0 if x else 1 - p0))
            if lam >= b:
                want = ("reject H0", i)
                break
            if lam <= a:
                want = ("accept H0", i)
                break
        assert sprt(seq, lf0, lf1, alpha, beta)[:2] == want
