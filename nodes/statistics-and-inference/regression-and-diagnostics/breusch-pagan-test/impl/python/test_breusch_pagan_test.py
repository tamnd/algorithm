# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breusch-pagan-test/. The authors are listed in prov/R9XRKX.jsonl.

import math
import random
from fractions import Fraction

import pytest

from breusch_pagan_test import breusch_pagan, monte_carlo_p_values
from stdist import chi2_ppf

EX_XS = list(range(1, 11))
EX_X = [[1, v] for v in EX_XS]
EX_Y = [Fraction(v) for v in ["3.2", "3.8", "5.5", "5.5", "8", "7", "11", "8", "14", "9"]]


def solve(a, b):
    k = len(a)
    m = [[Fraction(v) for v in row] + [Fraction(b[i])] for i, row in enumerate(a)]
    for c in range(k):
        piv = next(r for r in range(c, k) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [m[i][k] / m[i][i] for i in range(k)]


def ls_fit(x, y):
    """Exact least squares by the normal equations: coefficients and residuals."""
    p = len(x[0])
    gram = [[sum(Fraction(r[i]) * r[j] for r in x) for j in range(p)] for i in range(p)]
    b = solve(gram, [sum(Fraction(r[i]) * v for r, v in zip(x, y)) for i in range(p)])
    return b, [Fraction(v) - sum(Fraction(a) * c for a, c in zip(r, b)) for r, v in zip(x, y)]


def exact_statistics(x, y, z):
    """The auxiliary regression done directly: returns (LM_BP, LM_K, sigma2, v) as Fractions."""
    n = len(x)
    _, e = ls_fit(x, y)
    sigma2 = sum(t * t for t in e) / n
    g = [t * t / sigma2 for t in e]
    zz = [[1] + list(r) for r in z]
    _, u = ls_fit(zz, g)
    gbar = sum(g) / n
    tss = sum((t - gbar) ** 2 for t in g)
    ess = tss - sum(t * t for t in u)
    v = sum((t * t - sigma2) ** 2 for t in e) / n
    return ess / 2, n * ess / tss, sigma2, v, e, g


def test_page_example_exact():
    lm_bp, lm_k, sigma2, v, e, g = exact_statistics(EX_X, EX_Y, [[t] for t in EX_XS])
    assert sum(g) == len(g)  # the mean of g is exactly 1 because sigma2 is RSS / n
    res = breusch_pagan(EX_X, [float(t) for t in EX_Y])
    assert res.lm_bp == pytest.approx(float(lm_bp), rel=1e-10)
    assert res.lm_koenker == pytest.approx(float(lm_k), rel=1e-10)
    assert res.lm_bp == pytest.approx(5.1931, abs=1e-4)
    assert res.lm_koenker == pytest.approx(6.8880, abs=1e-4)
    assert res.p_bp == pytest.approx(0.02268, abs=1e-5)
    assert res.p_koenker == pytest.approx(0.008678, abs=1e-6)
    assert float(v / (2 * sigma2 ** 2)) == pytest.approx(0.75394, abs=1e-5)


def test_identities_exact():
    """LM_BP = LM_K v / (2 sigma2^2); LM_K = n R^2 for e^2 itself; LM_BP is the score form."""
    rng = random.Random(21)
    for _ in range(8):
        n = rng.randint(8, 14)
        x = [[1, rng.randint(-5, 5), rng.randint(0, 4)] for _ in range(n)]
        z = [[r[1], r[1] * r[1]] for r in x]
        y = [rng.randint(-9, 9) for _ in range(n)]
        try:
            lm_bp, lm_k, sigma2, v, e, g = exact_statistics(x, y, z)
        except (StopIteration, ZeroDivisionError):
            continue
        assert lm_bp == lm_k * v / (2 * sigma2 * sigma2)
        # R^2 does not change when the response e_i^2 is divided by sigma2.
        sq = [t * t for t in e]
        _, u = ls_fit([[1] + r for r in z], sq)
        mean = sum(sq) / n
        assert lm_k == n * (1 - sum(t * t for t in u) / sum((t - mean) ** 2 for t in sq))
        # Score form: (1/2) (g - 1)^T Z (Z^T Z)^(-1) Z^T (g - 1), with Z including the intercept.
        zz = [[1] + r for r in z]
        w = [t - 1 for t in g]
        coef = solve([[sum(Fraction(r[i]) * r[j] for r in zz) for j in range(3)] for i in range(3)],
                     [sum(r[i] * t for r, t in zip(zz, w)) for i in range(3)])
        assert lm_bp == sum(c * sum(r[i] * t for r, t in zip(zz, w)) for i, c in enumerate(coef)) / 2
        res = breusch_pagan(x, y, z)
        assert (res.lm_bp, res.lm_koenker) == pytest.approx((float(lm_bp), float(lm_k)), rel=1e-9)


def test_invariant_to_b_and_sigma_exact():
    """The residuals of a y + X c are a e, and both statistics are unchanged by the scale a."""
    z = [[t] for t in EX_XS]
    base = exact_statistics(EX_X, EX_Y, z)[:2]
    for a, c in ((Fraction(-3), (5, 2)), (Fraction(1, 7), (-1, 4))):
        y2 = [a * yi + c[0] + c[1] * xi for yi, xi in zip(EX_Y, EX_XS)]
        assert exact_statistics(EX_X, y2, z)[:2] == base


def test_bad_inputs():
    with pytest.raises(ValueError):
        breusch_pagan(EX_X, [1.0] * 9)
    with pytest.raises(ValueError):
        breusch_pagan(EX_X, [2.0 * t for t in EX_XS])  # a perfect fit: all residuals are 0


def test_monte_carlo_p_value_of_example_measured():
    """With 9999 normal samples the Monte Carlo p-values were 0.0077 and 0.0020; here B = 1999
    (4 SE about 0.008 and 0.004)."""
    p_bp, p_k = monte_carlo_p_values(EX_X, [float(t) for t in EX_Y], [[t] for t in EX_XS], reps=1999, seed=7)
    assert abs(p_bp - 0.0077) <= 0.008
    assert abs(p_k - 0.0020) <= 0.004


def run(rng, r, n, heavy, scale):
    xs = [rng.uniform(0.0, 1.0) for _ in range(n)]
    x = [[1.0, a] for a in xs]
    crit = chi2_ppf(0.95, 1)
    rej_bp = rej_k = 0
    for _ in range(r):
        if heavy:
            eps = [rng.gauss(0.0, 1.0) / math.sqrt(sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(5)) / 5)
                   for _ in range(n)]
        else:
            eps = [rng.gauss(0.0, 1.0) for _ in range(n)]
        y = [1.0 + 2.0 * a + t * scale(a) for a, t in zip(xs, eps)]
        res = breusch_pagan(x, y)
        rej_bp += res.lm_bp >= crit
        rej_k += res.lm_koenker >= crit
    return rej_bp / r, rej_k / r


def test_size_and_power_measured():
    """n = 50, one uniform regressor, 5% level. Measured with r = 4000 under H0: normal errors
    BP 0.048 and Koenker 0.054; t_5 errors BP 0.147 and Koenker 0.046. Power with sd 0.5 + 2x
    (r = 2000): normal 0.861 and 0.805. Here r = 1500 under H0 (4 SE about 0.023) and r = 400 for power."""
    flat = lambda a: 1.0
    bp, k = run(random.Random(1), 1500, 50, False, flat)
    assert abs(bp - 0.05) <= 0.023 and abs(k - 0.05) <= 0.023
    bp, k = run(random.Random(2), 1500, 50, True, flat)
    assert bp >= 0.10 and abs(k - 0.05) <= 0.023
    bp, k = run(random.Random(3), 400, 50, False, lambda a: 0.5 + 2.0 * a)
    assert bp >= 0.78 and k >= 0.72
