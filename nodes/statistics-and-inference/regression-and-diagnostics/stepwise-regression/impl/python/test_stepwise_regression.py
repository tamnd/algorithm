# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stepwise-regression/. The authors are listed in prov/GX5W9T.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from stdist import f_sf
from stepwise_regression import (
    aic, aicc, bic, centered_sscp, criterion_value, gaussian_loglik, stepwise, sweep,
)

# x1 and x2 are strongly correlated and y follows their difference, so each one alone is weak.
X1 = [1, -3, 3, -2, 2, -2, 1, 1, -2, 3]
X2 = [-1, -1, 3, -4, 0, -4, -1, 2, -4, 3]
X3 = [-2, -1, -3, 3, 1, -2, -1, -1, -3, -2]
Y = [-1, -3, -1, 4, 3, 0, 2, -2, 0, -1]
X = [[a, b, c] for a, b, c in zip(X1, X2, X3)]


def solve_exact(a, b):
    """Gauss-Jordan elimination in exact rational arithmetic."""
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


def fit_exact(x, y, s):
    """Least squares with an intercept and the columns s, from the normal equations: (coefficients, RSS)."""
    rows = [[Fraction(1)] + [Fraction(r[j]) for j in s] for r in x]
    k = len(rows[0])
    xtx = [[sum(r[i] * r[j] for r in rows) for j in range(k)] for i in range(k)]
    xty = [sum(r[i] * Fraction(v) for r, v in zip(rows, y)) for i in range(k)]
    b = solve_exact(xtx, xty)
    rss = sum((Fraction(v) - sum(bi * ri for bi, ri in zip(b, r))) ** 2 for r, v in zip(rows, y))
    return b, rss


def all_criteria(x, y, crit):
    n, p = len(y), len(x[0])
    return {s: criterion_value(float(fit_exact(x, y, s)[1]), n, len(s), crit)
            for r in range(p + 1) for s in itertools.combinations(range(p), r)}


def test_sweep_entries_and_reverse_sweep_are_exact():
    x = [[Fraction(v) for v in r] for r in X]
    y = [Fraction(v) for v in Y]
    a0 = centered_sscp(x, y)
    for r in range(4):
        for s in itertools.combinations(range(3), r):
            a = [row[:] for row in a0]
            for j in s:
                sweep(a, j)
            b, rss = fit_exact(X, Y, s)
            assert a[3][3] == rss
            for pos, j in enumerate(s):
                assert a[j][3] == b[pos + 1]
            for j in range(3):
                if j not in s:
                    toggled = fit_exact(X, Y, tuple(sorted(s + (j,))))[1]
                    assert a[3][3] - a[j][3] ** 2 / a[j][j] == toggled
            for j in reversed(s):
                sweep(a, j, reverse=True)
            assert a == a0


def test_forward_misses_the_best_subset_and_backward_finds_it():
    table = all_criteria(X, Y, "aic")
    best = min(table, key=table.get)
    assert best == (0, 1, 2)
    fwd = stepwise(X, Y, "forward", "aic")
    assert fwd.subset == (2,)
    assert table[fwd.subset] > table[best] + 10
    assert stepwise(X, Y, "backward", "aic").subset == best
    assert stepwise(X, Y, "both", "aic").subset == (2,)
    assert fit_exact(X, Y, (2,))[1] == Fraction(fwd.rss).limit_denominator(10**6)


def test_result_is_a_local_minimum_and_path_rss_is_exact():
    rng = random.Random(20261114)
    for _ in range(25):
        n, p = 14, 5
        x = [[rng.randint(-4, 4) for _ in range(p)] for _ in range(n)]
        y = [x[i][0] - x[i][2] + rng.randint(-3, 3) for i in range(n)]
        for crit in ("aic", "bic"):
            table = all_criteria(x, y, crit)
            for direction in ("forward", "backward", "both"):
                res = stepwise(x, y, direction, crit)
                s = set(res.subset)
                here = table[res.subset]
                for j in range(p):
                    t = tuple(sorted(s ^ {j}))
                    if direction == "forward" and j in s:
                        continue
                    if direction == "backward" and j not in s:
                        continue
                    assert table[t] >= here - 1e-9
                inside = set(range(p)) if direction == "backward" else set()
                for move, j, rss in res.path:
                    inside ^= {j}
                    assert math.isclose(rss, float(fit_exact(x, y, tuple(sorted(inside)))[1]), rel_tol=1e-9)


def test_orthogonal_columns_make_forward_selection_exact():
    # Columns of a 2^3 factorial design are orthogonal and centered, so RSS is additive in the columns.
    x = [[a, b, a * b] for a in (-1, 1) for b in (-1, 1) for _ in range(2)]
    rng = random.Random(7)
    for _ in range(30):
        y = [rng.randint(-5, 5) for _ in range(8)]
        for crit in ("aic", "bic"):
            table = all_criteria(x, y, crit)
            got = stepwise(x, y, "forward", crit).subset
            assert table[got] <= min(table.values()) + 1e-9


def test_information_criteria_match_their_formulas():
    n = len(Y)
    for s in [(), (2,), (0, 1, 2)]:
        b, rss = fit_exact(X, Y, s)
        s2 = rss / n
        resid = [Fraction(v) - b[0] - sum(b[i + 1] * Fraction(r[j]) for i, j in enumerate(s)) for r, v in zip(X, Y)]
        direct = math.fsum(-0.5 * math.log(2 * math.pi * float(s2)) - float(e * e / (2 * s2)) for e in resid)
        ll = gaussian_loglik(float(rss), n)
        assert math.isclose(ll, direct, rel_tol=1e-12)
        k = len(s) + 2
        assert math.isclose(aic(ll, k), -2 * direct + 2 * k, rel_tol=1e-12)
        assert math.isclose(bic(ll, k, n), -2 * direct + k * math.log(n), rel_tol=1e-12)
        assert math.isclose(aicc(ll, k, n), aic(ll, k) + 2 * k * (k + 1) / (n - k - 1), rel_tol=1e-12)
        assert math.isclose(criterion_value(float(rss), n, len(s), "aic"),
                            n * math.log(float(rss) / n) + n * (math.log(2 * math.pi) + 1) + 2 * k, rel_tol=1e-12)
    with pytest.raises(ValueError):
        aicc(0.0, 9, 10)


def test_f_rule_uses_partial_f_tests():
    n = len(Y)
    res = stepwise(X, Y, "forward", "f", alpha_enter=1.0)
    assert len(res.path) == 3
    first = res.path[0][1]
    rss0 = fit_exact(X, Y, ())[1]
    best_f = max(float(rss0 - fit_exact(X, Y, (j,))[1]) / (float(fit_exact(X, Y, (j,))[1]) / (n - 2)) for j in range(3))
    f_first = float(rss0 - fit_exact(X, Y, (first,))[1]) / (float(fit_exact(X, Y, (first,))[1]) / (n - 2))
    assert math.isclose(f_first, best_f)
    assert 0.0 < f_sf(f_first, 1, n - 2) < 1.0
    strict = stepwise(X, Y, "both", "f", alpha_enter=0.05, alpha_remove=0.10)
    assert strict.subset == (2,) and not strict.cycled
    back = stepwise(X, Y, "backward", "f", alpha_remove=0.10)
    assert back.subset == (0, 1, 2)


def test_bad_arguments():
    with pytest.raises(ValueError):
        stepwise(X, Y, "sideways")
    with pytest.raises(ValueError):
        stepwise(X, Y, "both", "cp")
    with pytest.raises(ValueError):
        centered_sscp([], [])
