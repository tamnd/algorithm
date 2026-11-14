# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yule-walker-equations/. The authors are listed in prov/Y7J377.jsonl.

import math
import random
from fractions import Fraction

import pytest

from yule_walker_equations import levinson_durbin, sample_autocovariance, sample_pacf, yule_walker


def solve_fraction(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    """Gaussian elimination with exact rational arithmetic (the brute force)."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        piv = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def ar_autocovariance_exact(phi: list[Fraction], sigma2: Fraction, max_lag: int) -> list[Fraction]:
    """gamma(0..max_lag) of a causal AR(p): solve the first p + 1 Yule-Walker equations
    in gamma(0..p) by elimination, then extend with the AR recursion."""
    p = len(phi)
    a = [[Fraction(0)] * (p + 1) for _ in range(p + 1)]
    b = [Fraction(0)] * (p + 1)
    for k in range(p + 1):  # gamma(k) - sum_j phi_j gamma(|k - j|) = sigma2 [k == 0]
        a[k][k] += 1
        for j in range(1, p + 1):
            a[k][abs(k - j)] -= phi[j - 1]
        b[k] = sigma2 if k == 0 else Fraction(0)
    g = solve_fraction(a, b)
    while len(g) <= max_lag:
        h = len(g)
        g.append(sum(phi[j - 1] * g[h - j] for j in range(1, p + 1)))
    return g[:max_lag + 1]


def simulate_ar(phi: list[float], n: int, rng: random.Random, burn: int = 300) -> list[float]:
    x = [0.0] * (n + burn)
    for t in range(n + burn):
        x[t] = rng.gauss(0.0, 1.0) + sum(phi[j] * x[t - 1 - j] for j in range(len(phi)) if t - 1 - j >= 0)
    return x[burn:]


def test_ar1_estimate_is_r1_over_r0_exactly():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(3, 15)
        x = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
        if len(set(x)) == 1:
            continue
        g = sample_autocovariance(x, 1)
        phi, s2 = yule_walker(x, 1)
        assert phi == [g[1] / g[0]]
        assert s2 == g[0] - g[1] ** 2 / g[0]


def test_levinson_matches_gaussian_elimination_in_fractions():
    rng = random.Random(2)
    for _ in range(40):
        n = rng.randint(8, 20)
        p = rng.randint(1, 5)
        x = [Fraction(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(n)]
        g = sample_autocovariance(x, p)
        mat = [[g[abs(i - j)] for j in range(p)] for i in range(p)]
        ref = solve_fraction(mat, g[1:p + 1])
        phi, v, _ = levinson_durbin(g, p)
        assert phi == ref
        assert v == g[0] - sum(a * b for a, b in zip(ref, g[1:p + 1]))


def test_exact_autocovariances_give_the_true_model_and_a_pacf_cut_off():
    cases = [
        [Fraction(1, 2), Fraction(3, 10)],
        [Fraction(1), Fraction(-1, 2)],
        [Fraction(-3, 5)],
        [Fraction(2, 5), Fraction(-1, 5), Fraction(1, 10)],
    ]
    for phi in cases:
        p = len(phi)
        g = ar_autocovariance_exact(phi, Fraction(2), p + 4)
        est, v, pacf = levinson_durbin(g, p + 4)
        assert est[:p] == phi and all(a == 0 for a in est[p:])
        assert v == 2
        assert all(a == 0 for a in pacf[p:])
        assert pacf[p - 1] == phi[-1]


def test_sample_autocovariance_by_hand():
    x = [Fraction(v) for v in (2, 4, 6, 5, 3)]
    assert sample_autocovariance(x, 2) == [Fraction(2), Fraction(1, 5), Fraction(-6, 5)]


def test_worked_example_numbers():
    x = [Fraction(v) for v in (3, 5, 6, 4, 2, 1, 3, 6, 7, 5)]
    g = sample_autocovariance(x, 2)
    assert g == [Fraction(84, 25), Fraction(207, 125), Fraction(-267, 250)]
    phi, v, pacf = levinson_durbin(g, 2)
    assert pacf[0] == Fraction(69, 140)
    assert phi == [Fraction(25461, 29678), Fraction(-10991, 14839)]
    assert v == Fraction(2129868, 1854875)


def test_fitted_model_is_causal():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(5, 40)
        p = rng.randint(1, min(6, n - 1))
        x = [rng.gauss(0, 1) + 3 * math.sin(t) for t in range(n)]
        pacf = sample_pacf(x, p)
        assert all(abs(a) < 1 for a in pacf)
        if p == 2:  # the stationarity triangle
            phi, _ = yule_walker(x, 2)
            assert phi[0] + phi[1] < 1 and phi[1] - phi[0] < 1 and abs(phi[1]) < 1


def test_monte_carlo_ar2_estimates_near_truth():
    # Measured, not proved: mean over r = 100 series of n = 400, seed 4.
    rng = random.Random(4)
    r, n = 100, 400
    s1 = s2 = 0.0
    for _ in range(r):
        phi, _ = yule_walker(simulate_ar([0.5, 0.3], n, rng), 2)
        s1 += phi[0]
        s2 += phi[1]
    # The asymptotic standard deviation of each estimate is sqrt((1 - 0.09) / 400) = 0.048,
    # so the standard error of the mean is 0.0048; allow 4 of them plus an O(1/n) bias of 0.02.
    assert abs(s1 / r - 0.5) < 0.04
    assert abs(s2 / r - 0.3) < 0.04


def test_errors():
    with pytest.raises(ValueError):
        yule_walker([1.0, 1.0, 1.0], 1)
    with pytest.raises(ValueError):
        sample_autocovariance([1.0, 2.0], 2)
    with pytest.raises(ValueError):
        levinson_durbin([Fraction(1), Fraction(1)], 1)
