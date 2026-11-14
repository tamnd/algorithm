# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shapiro-wilk-test/. The authors are listed in prov/F6R58F.jsonl.

import math
import random
from statistics import NormalDist

import pytest

from shapiro_wilk_test import shapiro_wilk, shapiro_wilk_coefficients

_N = NormalDist()


def exact_coefficients(n: int, h: float = 0.01, half_width: float = 8.0):
    """Brute force: a = V^(-1) m / ||V^(-1) m|| from the order statistic integrals.

    m_i = E Y_(i) and E Y_(i) Y_(j) for standard normal order statistics, by the
    trapezoid rule on [-half_width, half_width]. The double integral for i < j
    uses (F(v) - F(u))^d = sum_t C(d, t) F(v)^t (-F(u))^(d - t) and suffix sums.
    """
    xs = [-half_width + h * k for k in range(int(round(2 * half_width / h)) + 1)]
    K = len(xs)
    f = [_N.pdf(v) for v in xs]
    F = [_N.cdf(v) for v in xs]
    w = [h] * K
    w[0] = w[-1] = h / 2
    lg = math.lgamma

    def single(i: int, power: int) -> float:
        c = math.exp(lg(n + 1) - lg(i) - lg(n - i + 1))
        return sum(w[k] * xs[k] ** power * c * F[k] ** (i - 1) * (1 - F[k]) ** (n - i) * f[k]
                   for k in range(K))

    m = [single(i, 1) for i in range(1, n + 1)]
    e2 = [[0.0] * n for _ in range(n)]
    for i in range(1, n + 1):
        e2[i - 1][i - 1] = single(i, 2)
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            d = j - i - 1
            c = math.exp(lg(n + 1) - lg(i) - lg(d + 1) - lg(n - j + 1))
            total = 0.0
            for t in range(d + 1):
                g = [xs[k] * F[k] ** t * (1 - F[k]) ** (n - j) * f[k] for k in range(K)]
                suffix, acc = [0.0] * K, 0.0  # suffix[k] = trapezoid integral of g on [x_k, end]
                for k in range(K - 1, -1, -1):
                    if k < K - 1:
                        acc += 0.5 * h * (g[k] + g[k + 1])
                    suffix[k] = acc
                total += math.comb(d, t) * sum(
                    w[k] * xs[k] * F[k] ** (i - 1) * f[k] * (-F[k]) ** (d - t) * suffix[k]
                    for k in range(K))
            e2[i - 1][j - 1] = e2[j - 1][i - 1] = c * total
    v = [[e2[i][j] - m[i] * m[j] for j in range(n)] for i in range(n)]
    aug = [row[:] + [m[i]] for i, row in enumerate(v)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[piv] = aug[piv], aug[col]
        for r in range(n):
            if r != col:
                fac = aug[r][col] / aug[col][col]
                aug[r] = [a - fac * b for a, b in zip(aug[r], aug[col])]
    y = [aug[i][n] / aug[i][i] for i in range(n)]
    norm = math.sqrt(sum(t * t for t in y))
    return v, [t / norm for t in y]


def direct_w(x: list[float], a: list[float]) -> float:
    """Brute force: W as the squared correlation of the sorted sample with a."""
    y = sorted(x)
    n = len(y)
    ya, aa = sum(y) / n, sum(a) / n
    sxy = sum((p - ya) * (q - aa) for p, q in zip(y, a))
    sxx = sum((p - ya) ** 2 for p in y)
    syy = sum((q - aa) ** 2 for q in a)
    return sxy * sxy / (sxx * syy)


def test_worked_example() -> None:
    x = [148, 154, 158, 160, 161, 162, 166, 170, 182, 195, 236]
    w, p = shapiro_wilk(x)
    assert w == pytest.approx(0.78881, abs=1e-5)
    assert p == pytest.approx(0.006704, abs=2e-6)
    assert shapiro_wilk(x[:-1])[0] == pytest.approx(0.9080, abs=1e-4)


def test_coefficients_against_exact_order_statistic_integrals() -> None:
    for n in (4, 5, 6):
        v, exact = exact_coefficients(n)
        for row in v:  # for normal order statistics each row of V sums to 1
            assert sum(row) == pytest.approx(1.0, abs=1e-5)
        approx = shapiro_wilk_coefficients(n)
        assert max(abs(p - q) for p, q in zip(approx, exact)) < 1.5e-3


def test_coefficient_properties() -> None:
    for n in (3, 4, 5, 6, 7, 11, 12, 30, 101, 500):
        a = shapiro_wilk_coefficients(n)
        assert sum(t * t for t in a) == pytest.approx(1.0, abs=1e-12)
        assert all(a[i] == pytest.approx(-a[n - 1 - i], abs=1e-15) for i in range(n))
        assert all(a[i] < a[i + 1] for i in range(n - 1))


def test_w_against_direct_correlation_formula() -> None:
    rng = random.Random(41)
    for _ in range(50):
        n = rng.randint(3, 60)
        x = [rng.gauss(0.0, 1.0) if rng.random() < 0.5 else rng.expovariate(1.0) for _ in range(n)]
        w, p = shapiro_wilk(x)
        assert w == pytest.approx(direct_w(x, shapiro_wilk_coefficients(n)), rel=1e-12)
        assert 0.0 <= p <= 1.0


def test_location_scale_invariance_and_bounds() -> None:
    rng = random.Random(42)
    for _ in range(40):
        n = rng.randint(3, 40)
        x = [rng.gauss(5.0, 2.0) for _ in range(n)]
        w, p = shapiro_wilk(x)
        w2, p2 = shapiro_wilk([3.0 - 7.5 * t for t in x])
        assert w2 == pytest.approx(w, rel=1e-12) and p2 == pytest.approx(p, rel=1e-9, abs=1e-15)
        an = shapiro_wilk_coefficients(n)[-1]
        assert n * an * an / (n - 1) - 1e-12 <= w <= 1.0
        # The bound is attained by n - 1 equal values and one different value.
        assert shapiro_wilk([0.0] * (n - 1) + [1.0])[0] == pytest.approx(n * an * an / (n - 1), rel=1e-12)


def test_n3_null_distribution_is_exact() -> None:
    assert shapiro_wilk([0.0, 0.0, 1.0])[0] == pytest.approx(0.75)
    assert shapiro_wilk([0.0, 0.0, 1.0])[1] == pytest.approx(0.0, abs=1e-12)
    assert shapiro_wilk([0.0, 1.0, 2.0]) == pytest.approx((1.0, 1.0))
    rng = random.Random(43)
    ps = [shapiro_wilk([rng.gauss(0.0, 1.0) for _ in range(3)])[1] for _ in range(20000)]
    for u in (0.05, 0.1, 0.5, 0.9):
        assert abs(sum(p <= u for p in ps) / len(ps) - u) < 0.012


def test_monte_carlo_size_and_power() -> None:
    rng = random.Random(44)
    reps = 1500
    for n in (10, 30):
        size = sum(shapiro_wilk([rng.gauss(0.0, 1.0) for _ in range(n)])[1] <= 0.05
                   for _ in range(reps)) / reps
        assert abs(size - 0.05) < 0.02
    power = sum(shapiro_wilk([rng.expovariate(1.0) for _ in range(30)])[1] <= 0.05
                for _ in range(300)) / 300
    assert power > 0.8


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        shapiro_wilk([1.0, 2.0])
    with pytest.raises(ValueError):
        shapiro_wilk([4.0, 4.0, 4.0, 4.0])
    with pytest.raises(ValueError):
        shapiro_wilk_coefficients(5001)
