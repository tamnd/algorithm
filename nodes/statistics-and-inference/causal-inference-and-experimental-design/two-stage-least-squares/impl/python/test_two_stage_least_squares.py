# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-stage-least-squares/. The authors are listed in prov/2XMPJR.jsonl.

import math
import random
import statistics
from fractions import Fraction as Fr

import pytest

from two_stage_least_squares import crossprod, column, first_stage_f, inverse, matmul, ols, sargan, solve, tsls

ONE = Fr(1)


def test_worked_example():
    z = [0, 0, 0, 0, 1, 1, 1, 1]
    d = [0, 0, 0, 1, 1, 1, 1, 0]
    y = [1, 2, 3, 6, 5, 6, 4, 2]
    x = [[ONE, Fr(v)] for v in d]
    zz = [[ONE, Fr(v)] for v in z]
    r = tsls([Fr(v) for v in y], x, zz)
    assert r.coef == [Fr(19, 8), Fr(5, 2)]
    assert r.first_stage == [[1, Fr(1, 4)], [0, Fr(1, 2)]]
    assert r.resid == [Fr(v, 8) for v in (-11, -3, 5, 9, 1, 9, -7, -3)]
    assert r.sigma2 == Fr(47, 48)
    assert r.cov[1][1] == Fr(47, 24) and r.cov_hc0[1][1] == Fr(47, 32)
    assert ols([Fr(v) for v in y], x) == [Fr(2), Fr(13, 4)]


def wald(y, d, z):
    y1 = [a for a, b in zip(y, z) if b == 1]
    y0 = [a for a, b in zip(y, z) if b == 0]
    d1 = [a for a, b in zip(d, z) if b == 1]
    d0 = [a for a, b in zip(d, z) if b == 0]
    return (sum(y1) / len(y1) - sum(y0) / len(y0)) / (sum(d1) / len(d1) - sum(d0) / len(d0))


def test_binary_instrument_equals_wald_ratio_exactly():
    rng = random.Random(1)
    done = 0
    while done < 200:
        n = rng.randint(4, 12)
        z = [i % 2 for i in range(n)]
        rng.shuffle(z)
        d = [Fr(rng.randint(0, 1)) for _ in range(n)]
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        try:
            target = wald(y, d, z)
        except ZeroDivisionError:
            continue
        r = tsls(y, [[ONE, v] for v in d], [[ONE, Fr(v)] for v in z])
        assert r.coef[1] == target
        assert r.coef[0] == sum(y) / n - target * sum(d) / n
        done += 1


def random_design(rng, n, k_exog, k_endog, l_excl):
    exog = [[ONE] + [Fr(rng.randint(-5, 5)) for _ in range(k_exog)] for _ in range(n)]
    excl = [[Fr(rng.randint(-5, 5)) for _ in range(l_excl)] for _ in range(n)]
    endog = [[sum(e) + sum(z) + Fr(rng.randint(-3, 3)) for _ in range(k_endog)] for e, z in zip(exog, excl)]
    x = [a + b for a, b in zip(exog, endog)]
    z = [a + b for a, b in zip(exog, excl)]
    y = [Fr(rng.randint(-20, 20)) for _ in range(n)]
    return y, x, z, exog, excl


def test_equals_the_two_literal_stages():
    """Regressing y on the first-stage fitted values gives the same b, but the residual variance of
    that second regression is not the 2SLS one (it uses X_hat instead of X)."""
    rng = random.Random(2)
    differ = 0
    for _ in range(60):
        y, x, z, _, _ = random_design(rng, rng.randint(8, 14), 1, 1, 2)
        try:
            r = tsls(y, x, z)
        except ValueError:
            continue
        xh = [[sum(zij * pj for zij, pj in zip(zr, col)) for col in zip(*solve(crossprod(z, z), crossprod(z, x)))] for zr in z]
        assert ols(y, xh) == r.coef
        naive = [yi - sum(a * b for a, b in zip(row, r.coef)) for yi, row in zip(y, xh)]
        differ += sum(v * v for v in naive) != sum(v * v for v in r.resid)
    assert differ > 50


def test_just_identified_is_the_simple_iv_formula():
    rng = random.Random(3)
    for _ in range(60):
        y, x, z, _, _ = random_design(rng, rng.randint(6, 12), 1, 2, 2)
        try:
            r = tsls(y, x, z)
            direct = [v[0] for v in solve(crossprod(z, x), crossprod(z, column(y)))]
        except ValueError:
            continue
        assert r.coef == direct


def test_instruments_equal_to_regressors_give_ols():
    rng = random.Random(4)
    for _ in range(60):
        n = rng.randint(5, 12)
        x = [[ONE] + [Fr(rng.randint(-6, 6)) for _ in range(2)] for _ in range(n)]
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        try:
            r = tsls(y, x, x)
            b = ols(y, x)
        except ValueError:
            continue
        assert r.coef == b
        # White's HC0 for OLS, computed directly
        bread = inverse(crossprod(x, x))
        u = [yi - sum(a * c for a, c in zip(row, b)) for yi, row in zip(y, x)]
        meat = [[sum(ui * ui * row[i] * row[j] for ui, row in zip(u, x)) for j in range(3)] for i in range(3)]
        assert r.cov_hc0 == matmul(matmul(bread, meat), bread)


def test_first_stage_f_with_one_instrument_is_t_squared():
    rng = random.Random(5)
    for _ in range(40):
        y, x, z, exog, excl = random_design(rng, rng.randint(7, 12), 1, 1, 1)
        d = [row[-1] for row in x]
        try:
            f, q, df, _ = first_stage_f(d, exog, excl)
            r = tsls(d, z, z)  # OLS of d on Z, with its homoskedastic variance
        except (ValueError, ZeroDivisionError):
            continue
        assert q == 1 and f == r.coef[-1] ** 2 / r.cov[-1][-1]


def simulate(rng, n, beta, pi, rho, invalid=0.0):
    """y = 1 + beta d + u, d = z' pi + v, corr(u, v) = rho, three N(0, 1) instruments.
    invalid adds that multiple of the first instrument to y (a direct effect)."""
    y, x, z = [], [], []
    for _ in range(n):
        zi = [rng.gauss(0, 1) for _ in range(3)]
        e1, e2 = rng.gauss(0, 1), rng.gauss(0, 1)
        u = e1
        v = rho * e1 + math.sqrt(1 - rho * rho) * e2
        d = sum(p * a for p, a in zip(pi, zi)) + v
        y.append(1 + beta * d + u + invalid * zi[0])
        x.append([1.0, d])
        z.append([1.0] + zi)
    return y, x, z


def test_consistent_where_ols_is_biased_and_sargan_size():
    """r = 300 samples of n = 200 (seed 2026), beta = 1, first stage pi = (0.5, 0.5, 0.5), rho = 0.6.
    OLS has limit 1 + 0.6/1.75 = 1.343. 2SLS mean within 4 SE + 0.02 of 1; HC0 interval coverage at
    least 0.90; Sargan rejection rate at 5% within 0.05 +- 4 SE (SE = 0.0126)."""
    rng = random.Random(2026)
    r_, est, olss, rej, cover = 300, [], [], 0, 0
    for _ in range(r_):
        y, x, z = simulate(rng, 200, 1.0, (0.5, 0.5, 0.5), 0.6)
        res = tsls(y, x, z)
        est.append(res.coef[1])
        olss.append(ols(y, x)[1])
        se = math.sqrt(res.cov_hc0[1][1])
        cover += abs(res.coef[1] - 1) <= 1.96 * se
        rej += sargan(res, z)[2] < 0.05
    assert abs(statistics.mean(est) - 1) < 4 * statistics.stdev(est) / math.sqrt(r_) + 0.02
    assert abs(statistics.mean(olss) - 1.343) < 0.02
    assert cover / r_ >= 0.90
    assert abs(rej / r_ - 0.05) < 4 * math.sqrt(0.05 * 0.95 / r_)


def test_sargan_detects_an_invalid_instrument():
    rng = random.Random(7)
    rej = 0
    for _ in range(100):
        y, x, z = simulate(rng, 200, 1.0, (0.5, 0.5, 0.5), 0.6, invalid=0.5)
        rej += sargan(tsls(y, x, z), z)[2] < 0.05
    assert rej >= 80


def test_input_checks():
    x = [[ONE, Fr(i)] for i in range(5)]
    with pytest.raises(ValueError):
        tsls([ONE] * 5, x, [[ONE]] * 5)  # fewer instruments than regressors
    with pytest.raises(ValueError):
        tsls([ONE] * 5, x, [[ONE, ONE]] * 5)  # the instrument is constant: Z'Z is singular
    with pytest.raises(ValueError):
        sargan(tsls([Fr(i * i) for i in range(5)], x, x), x)
