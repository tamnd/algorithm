# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kpss-test/. The authors are listed in prov/AWK28P.jsonl.

import math
import random
from fractions import Fraction

import pytest

from kpss_test import (KPSS_TABLE, autocovariances, bandwidth, bartlett, cvm_limit_sf, detrend,
                       kpss, long_run_variance, simulate_null, table_p_value)

EXAMPLE = [Fraction(v) for v in (3, 5, 4, 6, 8, 7, 9, 8)]


def brute_eta(x, case, ell):
    """Brute force in exact rationals: residuals from the normal equations,
    partial sums by direct summation, and the Bartlett sum term by term."""
    n = len(x)
    cols = [[Fraction(1)] * n] + ([[Fraction(t + 1) for t in range(n)]] if case == "ct" else [])
    k = len(cols)
    a = [[sum(p * q for p, q in zip(cols[i], cols[j])) for j in range(k)]
         + [sum(p * q for p, q in zip(cols[i], x))] for i in range(k)]
    if k == 1:
        b = [a[0][1] / a[0][0]]
    else:
        det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
        b = [(a[0][2] * a[1][1] - a[0][1] * a[1][2]) / det, (a[0][0] * a[1][2] - a[1][0] * a[0][2]) / det]
    e = [x[t] - sum(b[j] * cols[j][t] for j in range(k)) for t in range(n)]
    num = sum(sum(e[:t + 1]) ** 2 for t in range(n))
    s2 = sum(v * v for v in e) / n
    for j in range(1, ell + 1):
        s2 += 2 * (1 - Fraction(j, ell + 1)) * sum(e[t] * e[t - j] for t in range(j, n)) / n
    return num / (n * n * s2)


def test_worked_example() -> None:
    r = kpss(EXAMPLE, "c", 0)
    assert r["eta"] == Fraction(235, 336)
    assert r["reject"]
    assert kpss(EXAMPLE, "c", 1)["eta"] == Fraction(235, 498)
    assert kpss(EXAMPLE, "c", 2)["eta"] == Fraction(2115, 5584)
    assert not kpss(EXAMPLE, "c", 2)["reject"]
    assert kpss(EXAMPLE, "ct", 0)["eta"] == Fraction(7, 104)
    assert kpss(EXAMPLE, "ct", 1)["eta"] == Fraction(7, 52)


@pytest.mark.parametrize("case", ["c", "ct"])
@pytest.mark.parametrize("ell", [0, 1, 2, 5])
def test_matches_brute_force(case, ell) -> None:
    rng = random.Random(10 * ell + len(case))
    x = [Fraction(rng.randint(-30, 30), rng.randint(1, 4)) for _ in range(17)]
    assert kpss(x, case, ell)["eta"] == brute_eta(x, case, ell)


@pytest.mark.parametrize("case", ["c", "ct"])
def test_residuals_are_orthogonal(case) -> None:
    # S_n = 0 always, and sum t e_t = 0 in case "ct".
    rng = random.Random(3)
    x = [Fraction(rng.randint(-9, 9)) for _ in range(12)]
    e = detrend(x, case)
    assert sum(e) == 0
    if case == "ct":
        assert sum((t + 1) * v for t, v in enumerate(e)) == 0


def test_bartlett_estimate_is_nonnegative() -> None:
    # The Bartlett weights give a nonnegative long-run variance for every series.
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(3, 15)
        e = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        for ell in range(n):
            assert long_run_variance(e, ell) >= 0
    # Truncated uniform weights can go negative: e = (1, -1, 1, -1), l = 1.
    gam = autocovariances([1, -1, 1, -1], 1)
    assert gam[0] + 2 * gam[1] < 0
    assert bartlett(gam) >= 0


@pytest.mark.parametrize("case,move", [("c", lambda t, v: 5 - 2 * v), ("ct", lambda t, v: 1 + 3 * t + 0.5 * v)])
def test_invariance(case, move) -> None:
    rng = random.Random(8)
    x = [rng.gauss(0, 1) for _ in range(50)]
    y = [move(t, v) for t, v in enumerate(x)]
    for ell in (0, 3, 12):
        assert abs(kpss(x, case, ell)["eta"] - kpss(y, case, ell)["eta"]) < 1e-9


def test_mean_of_numerator() -> None:
    # Var(S_t) = t (n - t) / n for iid unit-variance errors in case "c", so
    # E sum S_t^2 / n^2 = (n^2 - 1) / (6 n^2). Checked from the exact covariance of e.
    n = 9
    m = [[Fraction(int(i == j)) - Fraction(1, n) for j in range(n)] for i in range(n)]
    for t in range(1, n + 1):
        var = sum(m[i][j] for i in range(t) for j in range(t))
        assert var == Fraction(t * (n - t), n)
    total = sum(Fraction(t * (n - t), n) for t in range(1, n + 1))
    assert total / n ** 2 == Fraction(n * n - 1, 6 * n * n)


def test_bandwidth_rules() -> None:
    assert [bandwidth(n, "l4") for n in (50, 100, 200, 1000)] == [3, 4, 4, 7]
    assert [bandwidth(n, "l12") for n in (50, 100, 200, 1000)] == [10, 12, 14, 21]
    assert bandwidth(100, 7) == 7


@pytest.mark.parametrize("case", ["c", "ct"])
def test_size_against_table(case) -> None:
    # iid N(0, 1), n = 200, l = 0, 2000 samples: the 5% rejection rate must be
    # within 4 binomial standard errors (0.0195) of 0.05.
    reps = 2000
    sims = simulate_null(200, case, 0, reps, random.Random(31 if case == "c" else 32))
    rate = sum(1 for v in sims if v > KPSS_TABLE[case][0.05]) / reps
    assert abs(rate - 0.05) < 4 * math.sqrt(0.05 * 0.95 / reps)


def test_asymptotic_level_case() -> None:
    # The level-case limit is the Cramer-von Mises law. Its exact 5% point is
    # 0.4614 (Anderson and Darling 1952); the KPSS table rounds a simulation to 0.463.
    assert abs(cvm_limit_sf(0.4614) - 0.05) < 2e-4
    assert abs(cvm_limit_sf(0.3473) - 0.10) < 2e-4
    assert abs(cvm_limit_sf(0.7435) - 0.01) < 2e-4
    assert abs(cvm_limit_sf(0.463) - 0.05) < 1e-3


def test_power_against_random_walk() -> None:
    rng = random.Random(9)
    rej = 0
    for _ in range(50):
        s, y = 0.0, []
        for _ in range(200):
            s += rng.gauss(0, 1)
            y.append(s)
        rej += kpss(y, "c", "l4")["reject"]
    assert rej >= 40


def test_table_p_value() -> None:
    assert table_p_value(0.2) == 0.10
    assert table_p_value(0.463) == 0.05
    assert table_p_value(2.0) == 0.01
    assert abs(table_p_value((0.347 + 0.463) / 2) - 0.075) < 1e-12
    assert table_p_value(0.146, "ct") == 0.05


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        kpss([1, 2], "c", 0)
    with pytest.raises(ValueError):
        kpss([1, 1, 1, 1], "c", 0)
    with pytest.raises(ValueError):
        kpss([1, 2, 3, 5], "x", 0)
