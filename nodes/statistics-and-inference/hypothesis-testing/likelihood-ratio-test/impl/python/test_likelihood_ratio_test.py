# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-ratio-test/. The authors are listed in prov/04CJ2P.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from likelihood_ratio_test import (binomial_lrt, deviance_term, likelihood_ratio_test,
                                   most_powerful_test, multinomial_lrt, normal_mean_lrt,
                                   poisson_lrt)
from stdist import chi2_sf


def grid_argmax(f, lo: float, hi: float, steps: int = 200, rounds: int = 10) -> float:
    """Brute force: maximize a unimodal f on [lo, hi] by a grid, then shrink around the best point."""
    for _ in range(rounds):
        h = (hi - lo) / steps
        best = max(range(steps + 1), key=lambda i: f(lo + i * h))
        lo, hi = lo + max(best - 1, 0) * h, lo + min(best + 1, steps) * h
    return 0.5 * (lo + hi)


def test_worked_example() -> None:
    lam, p = binomial_lrt(15, 20, 0.5)
    exact = 2.0 * (15 * math.log(1.5) + 5 * math.log(0.5))
    assert abs(lam - exact) < 1e-12
    assert abs(lam - 5.232481) < 1e-6
    assert abs(p - 0.022169) < 1e-6


def test_binomial_against_brute_force_maximization() -> None:
    rng = random.Random(11)
    for _ in range(20):
        n = rng.randint(5, 60)
        k = rng.randint(1, n - 1)
        p0 = rng.uniform(0.05, 0.95)
        loglik = lambda p: k * math.log(p) + (n - k) * math.log(1.0 - p)
        lam, p = likelihood_ratio_test(loglik, lambda: grid_argmax(loglik, 1e-9, 1 - 1e-9),
                                       lambda: p0, 1)
        assert abs(lam - binomial_lrt(k, n, p0)[0]) < 1e-8 * max(1.0, lam)
        assert abs(p - binomial_lrt(k, n, p0)[1]) < 1e-8


def test_poisson_against_brute_force_maximization() -> None:
    rng = random.Random(12)
    for _ in range(20):
        n = rng.randint(1, 30)
        total = rng.randint(1, 100)
        lam0 = rng.uniform(0.2, 6.0)
        loglik = lambda t: total * math.log(t) - n * t
        lam, _ = likelihood_ratio_test(loglik, lambda: grid_argmax(loglik, 1e-9, 200.0),
                                       lambda: lam0, 1)
        assert abs(lam - poisson_lrt(total, n, lam0)[0]) < 1e-8 * max(1.0, lam)


def test_normal_unknown_variance_against_brute_force() -> None:
    rng = random.Random(13)
    for _ in range(3):
        n = rng.randint(3, 10)
        x = [rng.gauss(1.0, 2.0) for _ in range(n)]
        mu0 = rng.uniform(-1.0, 3.0)

        def loglik(theta: tuple[float, float]) -> float:
            mu, v = theta
            return -0.5 * n * math.log(v) - 0.5 * sum((xi - mu) ** 2 for xi in x) / v

        def profile_v(mu: float) -> float:
            return grid_argmax(lambda v: loglik((mu, v)), 1e-6, 100.0, steps=50, rounds=12)

        def fit_full() -> tuple[float, float]:
            mu = grid_argmax(lambda m: loglik((m, profile_v(m))), -10.0, 10.0, steps=20, rounds=15)
            return mu, profile_v(mu)

        lam, _ = likelihood_ratio_test(loglik, fit_full, lambda: (mu0, profile_v(mu0)), 1)
        closed, _ = normal_mean_lrt(x, mu0)
        assert abs(lam - closed) < 1e-6 * max(1.0, closed)
        mean = sum(x) / n
        s2 = sum((v - mean) ** 2 for v in x) / (n - 1)
        t = (mean - mu0) / math.sqrt(s2 / n)
        assert abs(closed - n * math.log1p(t * t / (n - 1))) < 1e-10 * max(1.0, closed)


def test_trinity_agrees_for_normal_mean_with_known_variance() -> None:
    rng = random.Random(14)
    for _ in range(50):
        n = rng.randint(1, 12)
        x = [rng.randint(-20, 20) for _ in range(n)]
        mu0, sigma = rng.randint(-5, 5), rng.randint(1, 6)
        # Exact: 2 (l(xbar) - l(mu0)) = (sum (x - mu0)^2 - sum (x - xbar)^2) / sigma^2.
        xbar = Fraction(sum(x), n)
        lr = (sum((Fraction(v) - mu0) ** 2 for v in x) - sum((v - xbar) ** 2 for v in x)) / sigma ** 2
        wald = (xbar - mu0) ** 2 / (Fraction(sigma ** 2) / n)  # (theta_hat - theta_0)^2 / Var
        u = sum(Fraction(v) - mu0 for v in x) / sigma ** 2  # score at mu0
        score = u * u / (Fraction(n) / sigma ** 2)  # U^2 / I_n
        assert lr == wald == score
        lam, _ = normal_mean_lrt(x, mu0, sigma)
        assert abs(lam - float(lr)) < 1e-9 * max(1.0, float(lr))


def test_multinomial_g_statistic() -> None:
    counts, probs = [18, 30, 52], [0.25, 0.25, 0.5]
    lam, p = multinomial_lrt(counts, probs)
    direct = 2.0 * sum(c * math.log(c / (100 * q)) for c, q in zip(counts, probs))
    assert abs(lam - direct) < 1e-12
    assert abs(p - chi2_sf(direct, 2)) < 1e-14
    assert multinomial_lrt([0, 5, 5], [0.2, 0.4, 0.4])[0] == pytest.approx(
        2.0 * 10 * math.log(1 / 0.8), rel=1e-12)


def test_deviance_term_is_stable_near_equality() -> None:
    # x log(x / y) - x + y = y h(1 + d) with h(1 + d) ~ d^2 / 2; at d = 1e-9 the naive form cancels.
    y, d = 50.0, 1e-9
    assert deviance_term(y * (1 + d), y) == pytest.approx(y * d * d / 2, rel=1e-6)
    for x, y in [(3.0, 2.9), (7.0, 7.5), (0.0, 1.5), (40.0, 4.0)]:
        naive = (x * math.log(x / y) if x else 0.0) - x + y
        assert deviance_term(x, y) == pytest.approx(naive, rel=1e-12, abs=1e-15)
    assert deviance_term(5.0, 5.0) == 0.0


def test_exact_binomial_size_by_enumeration() -> None:
    crit = 3.841458820694124
    for n, expected in [(20, 0.041389), (100, 0.056888)]:
        size = sum(Fraction(math.comb(n, k), 2 ** n)
                   for k in range(n + 1) if binomial_lrt(k, n, 0.5)[0] >= crit)
        assert abs(float(size) - expected) < 1e-6


def test_monte_carlo_size_normal_unknown_variance() -> None:
    rng = random.Random(15)
    reps, n = 2000, 30
    rejections = sum(normal_mean_lrt([rng.gauss(3.0, 2.0) for _ in range(n)], 3.0)[1] <= 0.05
                     for _ in range(reps))
    # Exact size of this nominal 5% test at n = 30 is about 0.0545; the MC error is about 0.005.
    assert abs(rejections / reps - 0.0545) < 0.02


def lp_vertex_optimum(f0: list[Fraction], f1: list[Fraction], alpha: Fraction) -> Fraction:
    """Brute force: the best power over all vertices of {0 <= phi <= 1, sum phi f0 <= alpha}.

    A vertex is 0 or 1 at every point except at most one, which then spends the
    rest of the size budget. The LP optimum is attained at a vertex.
    """
    m, best = len(f0), Fraction(0)
    for ones in itertools.product((0, 1), repeat=m):
        size = sum(f for f, o in zip(f0, ones) if o)
        if size > alpha:
            continue
        power = sum(f for f, o in zip(f1, ones) if o)
        best = max(best, power)
        for j in range(m):
            if not ones[j] and f0[j] > 0:
                frac = min(Fraction(1), (alpha - size) / f0[j])
                best = max(best, power + frac * f1[j])
    return best


def test_most_powerful_test_hand_example() -> None:
    f0 = [Fraction(4, 10), Fraction(3, 10), Fraction(2, 10), Fraction(1, 10)]
    f1 = [Fraction(1, 10), Fraction(2, 10), Fraction(3, 10), Fraction(4, 10)]
    phi = most_powerful_test(f0, f1, Fraction(1, 4))
    assert phi == [0, 0, Fraction(3, 4), 1]
    assert sum(p * f for p, f in zip(phi, f1)) == Fraction(5, 8)
    assert lp_vertex_optimum(f0, f1, Fraction(1, 4)) == Fraction(5, 8)


def test_most_powerful_test_against_all_vertex_tests() -> None:
    rng = random.Random(16)
    for _ in range(60):
        m = rng.randint(2, 6)
        w0 = [rng.randint(0, 6) for _ in range(m)]
        w1 = [rng.randint(0, 6) for _ in range(m)]
        if sum(w0) == 0 or sum(w1) == 0:
            continue
        f0 = [Fraction(w, sum(w0)) for w in w0]
        f1 = [Fraction(w, sum(w1)) for w in w1]
        alpha = Fraction(rng.randint(0, 20), 20)
        phi = most_powerful_test(f0, f1, alpha)
        assert all(0 <= p <= 1 for p in phi)
        assert sum(p * f for p, f in zip(phi, f0)) <= alpha
        power = sum(p * f for p, f in zip(phi, f1))
        assert power == lp_vertex_optimum(f0, f1, alpha)


def test_simple_likelihood_ratio_is_an_e_variable_with_markov_bound() -> None:
    n, half, q = 10, Fraction(1, 2), Fraction(4, 5)
    prob = [Fraction(math.comb(n, k), 2 ** n) for k in range(n + 1)]
    e = [(q / half) ** k * ((1 - q) / half) ** (n - k) for k in range(n + 1)]
    assert sum(p * v for p, v in zip(prob, e)) == 1
    for alpha in [Fraction(1, 2), Fraction(1, 10), Fraction(1, 20), Fraction(1, 100)]:
        tail = sum(p for p, v in zip(prob, e) if v >= 1 / alpha)
        assert tail <= alpha
    assert sum(p for p, v in zip(prob, e) if v >= 20) == Fraction(11, 1024)


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        binomial_lrt(3, 2, 0.5)
    with pytest.raises(ValueError):
        normal_mean_lrt([1.0, 1.0, 1.0], 0.0)
    with pytest.raises(ValueError):
        multinomial_lrt([1, 2], [0.5, 0.6])
