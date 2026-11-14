# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wald-test/. The authors are listed in prov/QP1T8S.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from stdist import chi2_sf
from wald_test import (binomial_wald, logit_binomial_wald, normal_mean_wald, poisson_wald,
                       solve, wald_test)


def observed_information(loglik, theta: list[float]) -> list[list[float]]:
    """Brute force: minus the Hessian of loglik at theta, by central differences with
    steps relative to each coordinate and one Richardson extrapolation step."""
    k = len(theta)

    def hessian(scale: float) -> list[list[float]]:
        out = [[0.0] * k for _ in range(k)]
        for i in range(k):
            for j in range(k):
                hi, hj = scale * abs(theta[i]), scale * abs(theta[j])

                def at(si: int, sj: int) -> float:
                    t = list(theta)
                    t[i] += si * hi
                    t[j] += sj * hj
                    return loglik(t)
                out[i][j] = (at(1, 1) - at(1, -1) - at(-1, 1) + at(-1, -1)) / (4 * hi * hj)
        return out

    coarse, fine = hessian(2e-3), hessian(1e-3)
    return [[-(4 * fine[i][j] - coarse[i][j]) / 3 for j in range(k)] for i in range(k)]


def inverse_by_cofactors(a: list[list[Fraction]]) -> list[list[Fraction]]:
    """Brute force: the inverse by the adjugate, with determinants by permutation sums."""
    n = len(a)

    def det(m: list[list[Fraction]]) -> Fraction:
        total = Fraction(0)
        for perm in itertools.permutations(range(len(m))):
            sign = 1
            for i in range(len(perm)):
                for j in range(i + 1, len(perm)):
                    if perm[i] > perm[j]:
                        sign = -sign
            prod = Fraction(sign)
            for i, pi in enumerate(perm):
                prod *= m[i][pi]
            total += prod
        return total

    d = det(a)
    minor = lambda i, j: [row[:j] + row[j + 1:] for r, row in enumerate(a) if r != i]
    return [[(-1) ** (i + j) * det(minor(j, i)) / d for j in range(n)] for i in range(n)]


def test_worked_example() -> None:
    w, p = binomial_wald(15, 20, 0.5)
    assert w == pytest.approx(20 / 3, rel=1e-14)
    assert p == pytest.approx(0.009823, abs=1e-6)
    w2, p2 = wald_test([0.75], [0.5], [[0.75 * 0.25 / 20]])
    assert w2 == pytest.approx(w, rel=1e-14) and p2 == pytest.approx(p, rel=1e-12)


def test_solver_is_exact_against_cofactor_inverse() -> None:
    rng = random.Random(21)
    for _ in range(30):
        r = rng.randint(1, 4)
        b = [[Fraction(rng.randint(-5, 5)) for _ in range(r)] for _ in range(r)]
        cov = [[sum(b[i][t] * b[j][t] for t in range(r)) + (1 if i == j else 0)
                for j in range(r)] for i in range(r)]  # B B^T + I is positive definite
        est = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(r)]
        null = [Fraction(rng.randint(-3, 3)) for _ in range(r)]
        w, p = wald_test(est, null, cov)
        inv = inverse_by_cofactors(cov)
        d = [e - z for e, z in zip(est, null)]
        assert w == sum(d[i] * inv[i][j] * d[j] for i in range(r) for j in range(r))
        assert p == pytest.approx(chi2_sf(float(w), r), rel=1e-15)


def test_binomial_and_poisson_against_numerical_observed_information() -> None:
    rng = random.Random(22)
    for _ in range(20):
        n = rng.randint(5, 80)
        k = rng.randint(1, n - 1)
        p0 = rng.uniform(0.05, 0.95)
        ll = lambda t: k * math.log(t[0]) + (n - k) * math.log(1.0 - t[0])
        info = observed_information(ll, [k / n])
        w, _ = wald_test([k / n], [p0], [[1.0 / info[0][0]]])
        assert w == pytest.approx(binomial_wald(k, n, p0)[0], rel=1e-5)
        total, lam0 = rng.randint(1, 100), rng.uniform(0.2, 6.0)
        llp = lambda t: total * math.log(t[0]) - n * t[0]
        info = observed_information(llp, [total / n])
        w, _ = wald_test([total / n], [lam0], [[1.0 / info[0][0]]])
        assert w == pytest.approx(poisson_wald(total, n, lam0)[0], rel=1e-5)


def test_normal_two_parameters_against_numerical_observed_information() -> None:
    rng = random.Random(23)
    for _ in range(10):
        n = rng.randint(3, 30)
        x = [rng.gauss(2.0, 1.5) for _ in range(n)]
        mean = sum(x) / n
        v = sum((t - mean) ** 2 for t in x) / n
        ll = lambda t: -0.5 * n * math.log(t[1]) - sum((xi - t[0]) ** 2 for xi in x) / (2 * t[1])
        info = observed_information(ll, [mean, v])
        det = info[0][0] * info[1][1] - info[0][1] * info[1][0]
        cov = [[info[1][1] / det, -info[0][1] / det], [-info[1][0] / det, info[0][0] / det]]
        mu0 = rng.uniform(0.0, 4.0)
        w1, _ = wald_test([mean], [mu0], [[cov[0][0]]])
        assert w1 == pytest.approx(normal_mean_wald(x, mu0)[0], rel=1e-5)
        v0 = rng.uniform(0.5, 4.0)
        w2, p2 = wald_test([mean, v], [mu0, v0], cov)
        closed = n * (mean - mu0) ** 2 / v + n * (v - v0) ** 2 / (2 * v * v)
        assert w2 == pytest.approx(closed, rel=1e-5)
        assert p2 == pytest.approx(chi2_sf(closed, 2), rel=1e-4, abs=1e-12)


def test_trinity_agrees_for_normal_mean_with_known_variance() -> None:
    rng = random.Random(24)
    for _ in range(50):
        n = rng.randint(1, 12)
        x = [rng.randint(-20, 20) for _ in range(n)]
        mu0, sigma = rng.randint(-5, 5), rng.randint(1, 6)
        xbar = Fraction(sum(x), n)
        wald, _ = wald_test([xbar], [Fraction(mu0)], [[Fraction(sigma * sigma, n)]])
        lr = (sum((Fraction(v) - mu0) ** 2 for v in x) - sum((v - xbar) ** 2 for v in x)) / sigma ** 2
        u = sum(Fraction(v) - mu0 for v in x) / sigma ** 2
        score = u * u / (Fraction(n) / sigma ** 2)
        assert wald == lr == score
        assert normal_mean_wald(x, mu0, sigma)[0] == pytest.approx(float(wald), rel=1e-12, abs=1e-15)


def test_trinity_order_for_normal_mean_with_unknown_variance() -> None:
    x = [502, 498, 505, 503, 501, 507, 499, 504, 506]
    w, p = normal_mean_wald(x, 500)
    assert w == pytest.approx(8.2721, abs=1e-4) and p == pytest.approx(0.00403, abs=1e-5)
    rng = random.Random(25)
    for _ in range(100):
        n = rng.randint(2, 20)
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        mean = sum(x) / n
        ss = sum((t - mean) ** 2 for t in x)
        u = n * mean ** 2 / ss  # T^2 / (n - 1) for mu0 = 0
        w = normal_mean_wald(x, 0.0)[0]
        assert w == pytest.approx(n * u, rel=1e-10)
        assert w >= n * math.log1p(u) >= n * u / (1 + u)  # W >= LR >= score


def test_not_invariant_under_reparametrization() -> None:
    assert binomial_wald(15, 20, 0.5)[0] == pytest.approx(6.6667, abs=1e-4)
    assert logit_binomial_wald(15, 20, 0.5)[0] == pytest.approx(4.5261, abs=1e-4)


def test_hauck_donner_effect_on_the_logit_scale() -> None:
    w = {k: logit_binomial_wald(k, 20, 0.5)[0] for k in range(11, 20)}
    assert w[18] == pytest.approx(8.69, abs=1e-2)
    assert w[19] < w[18]  # the statistic falls as the evidence grows
    assert all(w[k] < w[k + 1] for k in range(11, 18))
    p_scale = [binomial_wald(k, 20, 0.5)[0] for k in range(10, 20)]
    assert all(a < b for a, b in zip(p_scale, p_scale[1:]))
    with pytest.raises(ValueError):
        logit_binomial_wald(20, 20, 0.5)


def test_exact_binomial_size_by_enumeration() -> None:
    crit = 3.841458820694124
    for n, p0, expected in [(10, Fraction(1, 2), 0.1094), (20, Fraction(1, 2), 0.0414),
                            (20, Fraction(1, 10), 0.1240), (30, Fraction(1, 20), 0.2179)]:
        size = sum(math.comb(n, k) * p0 ** k * (1 - p0) ** (n - k)
                   for k in range(n + 1) if binomial_wald(k, n, float(p0))[0] >= crit)
        assert abs(float(size) - expected) < 1e-4


def test_monte_carlo_size_poisson() -> None:
    rng = random.Random(26)
    reps, n, lam0 = 3000, 50, 2.0
    hits = 0
    for _ in range(reps):
        total = 0
        for _ in range(n):  # Poisson(lam0) by counting unit-rate arrivals
            t = rng.expovariate(lam0)
            while t < 1.0:
                total += 1
                t += rng.expovariate(lam0)
        hits += poisson_wald(total, n, lam0)[1] <= 0.05
    assert abs(hits / reps - 0.05) < 0.02


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        wald_test([1.0, 2.0], [0.0], [[1.0]])
    with pytest.raises(ValueError):
        solve([[1.0, 2.0], [2.0, 4.0]], [1.0, 1.0])
    with pytest.raises(ValueError):
        normal_mean_wald([3.0, 3.0], 0.0)
    assert binomial_wald(0, 10, 0.3) == (math.inf, 0.0)
