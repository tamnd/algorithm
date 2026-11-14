# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/score-test/. The authors are listed in prov/6H761T.jsonl.

import math
import random
from fractions import Fraction

import pytest

from score_test import (binomial_score, multinomial_score, normal_mean_score, poisson_score,
                        score_test, solve)
from stdist import chi2_sf, norm_ppf


def numeric_score(loglik, theta: list[float]) -> list[float]:
    """Brute force: the gradient of loglik by central differences with Richardson extrapolation."""
    out = []
    for i in range(len(theta)):
        def diff(h: float) -> float:
            up, dn = list(theta), list(theta)
            up[i] += h
            dn[i] -= h
            return (loglik(up) - loglik(dn)) / (2 * h)
        h = 1e-3 * max(abs(theta[i]), 1e-3)
        out.append((4 * diff(h / 2) - diff(h)) / 3)
    return out


def expected_information(one_loglik, theta: float, support) -> float:
    """Brute force: Var of the one-observation score, by summing over the support."""
    total = 0.0
    for x, prob in support:
        u = numeric_score(lambda t: one_loglik(x, t[0]), [theta])[0]
        total += prob * u * u
    return total


def test_worked_example() -> None:
    s, p = binomial_score(15, 20, 0.5)
    assert s == pytest.approx(5.0, rel=1e-14)
    assert p == pytest.approx(0.025347, abs=1e-6)
    z = (15 - 10) / math.sqrt(20 * 0.25)
    assert s == pytest.approx(z * z, rel=1e-14)  # the one-proportion z-test squared


def test_binomial_and_poisson_against_numerical_score_and_information() -> None:
    rng = random.Random(31)
    for _ in range(15):
        n = rng.randint(5, 60)
        k = rng.randint(0, n)
        p0 = rng.uniform(0.05, 0.95)
        ll = lambda t: k * math.log(t[0]) + (n - k) * math.log(1.0 - t[0])
        one = lambda x, p: x * math.log(p) + (1 - x) * math.log(1.0 - p)
        info = n * expected_information(one, p0, [(0, 1 - p0), (1, p0)])
        s, _ = score_test(lambda t: numeric_score(ll, t), lambda t: [[info]], lambda: [p0], 1)
        assert s == pytest.approx(binomial_score(k, n, p0)[0], rel=1e-6, abs=1e-9)
    for _ in range(10):
        n, total, lam0 = rng.randint(1, 20), rng.randint(0, 80), rng.uniform(0.5, 5.0)
        ll = lambda t: total * math.log(t[0]) - n * t[0]
        one = lambda x, lam: x * math.log(lam) - lam
        support = [(x, math.exp(-lam0 + x * math.log(lam0) - math.lgamma(x + 1))) for x in range(80)]
        info = n * expected_information(one, lam0, support)
        s, _ = score_test(lambda t: numeric_score(ll, t), lambda t: [[info]], lambda: [lam0], 1)
        assert s == pytest.approx(poisson_score(total, n, lam0)[0], rel=1e-6, abs=1e-9)


def test_normal_unknown_variance_against_numerical_score() -> None:
    rng = random.Random(32)
    for _ in range(20):
        n = rng.randint(2, 25)
        x = [rng.gauss(1.0, 2.0) for _ in range(n)]
        mu0 = rng.uniform(-1.0, 3.0)
        ll = lambda t: -0.5 * n * math.log(t[1]) - sum((v - t[0]) ** 2 for v in x) / (2 * t[1])
        fit_null = lambda: [mu0, sum((v - mu0) ** 2 for v in x) / n]
        info = lambda t: [[n / t[1], 0.0], [0.0, n / (2 * t[1] ** 2)]]
        s, _ = score_test(lambda t: numeric_score(ll, t), info, fit_null, 1)
        closed = normal_mean_score(x, mu0)[0]
        assert s == pytest.approx(closed, rel=1e-6, abs=1e-9)
        mean = sum(x) / n
        t2 = (mean - mu0) ** 2 / (sum((v - mean) ** 2 for v in x) / (n - 1) / n)
        assert closed == pytest.approx(n * t2 / (n - 1 + t2), rel=1e-10)


def test_multinomial_score_is_pearson_exactly() -> None:
    rng = random.Random(33)
    for _ in range(40):
        m = rng.randint(2, 5)
        w = [rng.randint(1, 6) for _ in range(m)]
        q = [Fraction(v, sum(w)) for v in w]
        counts = [rng.randint(0, 15) for _ in range(m)]
        n = sum(counts)
        if n == 0:
            continue
        # Free parameters q_1..q_(m-1); q_m = 1 - sum. Score and information at q.
        u = [Fraction(counts[j]) / q[j] - Fraction(counts[-1]) / q[-1] for j in range(m - 1)]
        info = [[n * ((1 / q[i] if i == j else 0) + 1 / q[-1]) for j in range(m - 1)]
                for i in range(m - 1)]
        s, p = score_test(lambda t: u, lambda t: info, lambda: q, m - 1)
        pearson = sum((c - n * qj) ** 2 / (n * qj) for c, qj in zip(counts, q))
        assert s == pearson
        got, pg = multinomial_score(counts, [float(v) for v in q])
        assert got == pytest.approx(float(pearson), rel=1e-12, abs=1e-14)
        assert pg == pytest.approx(p, rel=1e-10)


def test_trinity_agrees_for_normal_mean_with_known_variance() -> None:
    rng = random.Random(34)
    for _ in range(50):
        n = rng.randint(1, 12)
        x = [rng.randint(-20, 20) for _ in range(n)]
        mu0, sigma = rng.randint(-5, 5), rng.randint(1, 6)
        u = sum(Fraction(v) - mu0 for v in x) / sigma ** 2
        s, _ = score_test(lambda t: [u], lambda t: [[Fraction(n, sigma ** 2)]], lambda: [mu0], 1)
        xbar = Fraction(sum(x), n)
        lr = (sum((Fraction(v) - mu0) ** 2 for v in x) - sum((v - xbar) ** 2 for v in x)) / sigma ** 2
        wald = (xbar - mu0) ** 2 * n / sigma ** 2
        assert s == lr == wald
        assert normal_mean_score(x, mu0, sigma)[0] == pytest.approx(float(s), rel=1e-12, abs=1e-15)


def test_invariant_under_reparametrization() -> None:
    # The score test of p = p0 and of logit p = logit p0 give the same S with expected information.
    for k, n, p0 in [(15, 20, 0.5), (3, 40, 0.2), (0, 10, 0.3)]:
        b0 = math.log(p0 / (1 - p0))
        ll = lambda t: k * t[0] - n * math.log1p(math.exp(t[0]))  # log-likelihood in beta
        info = n * p0 * (1 - p0)
        s, _ = score_test(lambda t: numeric_score(ll, t), lambda t: [[info]], lambda: [b0], 1)
        assert s == pytest.approx(binomial_score(k, n, p0)[0], rel=1e-6)


def test_inverting_gives_the_wilson_interval() -> None:
    z = norm_ppf(0.975)
    for k, n in [(15, 20), (0, 10), (7, 9), (50, 120)]:
        ph = k / n
        centre = (ph + z * z / (2 * n)) / (1 + z * z / n)
        half = z / (1 + z * z / n) * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
        for end in (centre - half, centre + half):
            if 0.0 < end < 1.0:
                assert binomial_score(k, n, end)[0] == pytest.approx(z * z, rel=1e-9)
        assert binomial_score(k, n, min(max(centre, 1e-9), 1 - 1e-9))[0] < z * z


def test_exact_binomial_size_by_enumeration() -> None:
    crit = 3.841458820694124
    for n, p0, expected in [(10, Fraction(1, 2), 0.0215), (20, Fraction(1, 10), 0.0432),
                            (50, Fraction(1, 10), 0.0297), (30, Fraction(1, 20), 0.0608)]:
        size = sum(math.comb(n, k) * p0 ** k * (1 - p0) ** (n - k)
                   for k in range(n + 1) if binomial_score(k, n, float(p0))[0] >= crit)
        assert abs(float(size) - expected) < 1e-4


def test_monte_carlo_size_normal_unknown_variance() -> None:
    rng = random.Random(35)
    reps, n = 3000, 30
    hits = sum(normal_mean_score([rng.gauss(0.0, 3.0) for _ in range(n)], 0.0)[1] <= 0.05
               for _ in range(reps))
    assert abs(hits / reps - 0.05) < 0.02


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        score_test(lambda t: [1.0], lambda t: [[1.0]], lambda: [0.0], 0)
    with pytest.raises(ValueError):
        solve([[0.0]], [1.0])
    with pytest.raises(ValueError):
        multinomial_score([1, 2], [0.5, 0.6])
    assert chi2_sf(0.0, 1) == 1.0
