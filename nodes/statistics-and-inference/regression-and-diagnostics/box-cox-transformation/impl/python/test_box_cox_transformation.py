# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/box-cox-transformation/. The authors are listed in prov/KHKPKJ.jsonl.

import math
import random

import pytest

from box_cox_transformation import BoxCoxProfile, box_cox, box_cox_fit

Y8 = [0.1, 0.2, 0.4, 0.5, 0.9, 1.3, 2.0, 3.6]


def _solve(A, b):
    """Gauss-Jordan elimination with partial pivoting (the brute force for small p)."""
    m = len(A)
    M = [list(map(float, row)) + [float(v)] for row, v in zip(A, b)]
    for c in range(m):
        piv = max(range(c, m), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        for r in range(m):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][m] / M[i][i] for i in range(m)]


def _rss_normal_equations(X, z):
    p = len(X[0])
    XtX = [[math.fsum(row[i] * row[j] for row in X) for j in range(p)] for i in range(p)]
    Xtz = [math.fsum(row[i] * v for row, v in zip(X, z)) for i in range(p)]
    b = _solve(XtX, Xtz)
    return math.fsum((v - math.fsum(bi * xi for bi, xi in zip(b, row))) ** 2 for row, v in zip(X, z))


def _brute_loglik(y, X, lam):
    """l(lambda) from the plain transform and the normal equations."""
    z = [math.log(v) if lam == 0 else (v ** lam - 1.0) / lam for v in y]
    n = len(y)
    return -0.5 * n * math.log(_rss_normal_equations(X, z) / n) + (lam - 1.0) * math.fsum(map(math.log, y))


def _random_problem(rng, n, p):
    X = [[1.0] + [rng.uniform(0.0, 5.0) for _ in range(p - 1)] for _ in range(n)]
    lam0 = rng.choice([-0.5, 0.0, 0.5, 1.0])
    y = []
    for row in X:
        z = 0.2 * (2.0 + 0.4 * sum(row[1:]) + rng.gauss(0.0, 0.3))  # z in about (0.2, 1.3)
        y.append(math.exp(z) if lam0 == 0.0 else (1.0 + lam0 * z) ** (1.0 / lam0))
    return X, y


def test_worked_example() -> None:
    lam, lmax, a, b = box_cox_fit(Y8)
    assert abs(lam - 0.07784) < 1e-4
    assert abs(lmax - 2.53422) < 1e-4
    assert abs(a - (-0.58707)) < 1e-4 and abs(b - 0.76145) < 1e-4
    P = BoxCoxProfile(Y8)
    assert 2.0 * (lmax - P.loglik(1.0)) > 3.8415  # no transform is rejected
    assert 2.0 * (lmax - P.loglik(0.0)) < 3.8415  # the log is not


def test_profile_matches_plain_formula() -> None:
    rng = random.Random(1)
    for _ in range(60):
        n, p = rng.randint(6, 25), rng.randint(1, 4)
        X, y = _random_problem(rng, n, p)
        P = BoxCoxProfile(y, X)
        # No lambda near 0 here: the plain (y^lambda - 1) / lambda of the brute force cancels there.
        for lam in [-2.0, -1.0, -0.3, 0.0, 0.5, 1.0, 1.7, 2.0]:
            assert abs(P.loglik(lam) - _brute_loglik(y, X, lam)) < 1e-7 * (1.0 + abs(P.loglik(lam)))


def test_against_dense_grid() -> None:
    rng = random.Random(2)
    for _ in range(25):
        n, p = rng.randint(8, 20), rng.randint(1, 3)
        X, y = _random_problem(rng, n, p)
        lam, lmax, _, _ = box_cox_fit(y, X)
        grid = [-2.0 + 4.0 * j / 4000 for j in range(4001)]
        P = BoxCoxProfile(y, X)
        vals = [P.loglik(t) for t in grid]
        j = max(range(len(grid)), key=lambda i: vals[i])
        assert lmax >= vals[j] - 1e-9
        assert abs(lam - grid[j]) <= 1e-3 + 1e-9 or abs(lmax - vals[j]) < 1e-6


def test_profile_equals_maximized_full_likelihood() -> None:
    rng = random.Random(3)
    X, y = _random_problem(rng, 15, 3)
    n = len(y)
    P = BoxCoxProfile(y, X)
    for lam in [-1.0, 0.0, 0.4, 1.3]:
        z = box_cox(y, lam)
        p = len(X[0])
        XtX = [[math.fsum(r[i] * r[j] for r in X) for j in range(p)] for i in range(p)]
        b = _solve(XtX, [math.fsum(r[i] * v for r, v in zip(X, z)) for i in range(p)])
        res = [v - math.fsum(bi * xi for bi, xi in zip(b, r)) for r, v in zip(X, z)]
        s2 = math.fsum(e * e for e in res) / n
        full = math.fsum(-0.5 * math.log(2.0 * math.pi * s2) - e * e / (2.0 * s2) for e in res)
        full += (lam - 1.0) * math.fsum(map(math.log, y))
        # Perturbing b or sigma^2 can only lower the full likelihood.
        worse = math.fsum(-0.5 * math.log(2.0 * math.pi * s2 * 1.1) - (e + 0.01) ** 2 / (2.0 * s2 * 1.1) for e in res)
        worse += (lam - 1.0) * math.fsum(map(math.log, y))
        assert worse < full
        assert abs(full - (P.loglik(lam) - 0.5 * n * (math.log(2.0 * math.pi) + 1.0))) < 1e-9 * n


def test_scale_invariance_with_intercept() -> None:
    rng = random.Random(4)
    X, y = _random_problem(rng, 18, 2)
    a = box_cox_fit(y, X, lo=-8.0, hi=8.0)
    assert a[2] is not None and a[3] is not None
    for c in [1e-3, 7.0, 1e4]:
        b = box_cox_fit([c * v for v in y], X, lo=-8.0, hi=8.0)
        assert abs(a[0] - b[0]) < 1e-5
        assert abs(a[2] - b[2]) < 1e-5 and abs(a[3] - b[3]) < 1e-5
        # l changes by the constant -n log c.
        assert abs((b[1] - a[1]) + len(y) * math.log(c)) < 1e-6 * len(y)


def test_lambda_zero_is_continuous_and_lambda_one_is_a_shift() -> None:
    P = BoxCoxProfile(Y8)
    assert abs(P.loglik(1e-10) - P.loglik(0.0)) < 1e-8
    assert abs(P.loglik(-1e-10) - P.loglik(0.0)) < 1e-8
    m = sum(Y8) / len(Y8)
    rss = math.fsum((v - m) ** 2 for v in Y8)
    assert abs(P.loglik(1.0) - (-4.0 * math.log(rss / 8.0))) < 1e-12
    assert box_cox([math.e], 0.0) == [1.0]
    assert abs(box_cox([4.0], 0.5)[0] - 2.0) < 1e-15


def test_without_intercept_keeps_the_constant() -> None:
    rng = random.Random(5)
    n = 12
    X = [[rng.uniform(1.0, 3.0)] for _ in range(n)]
    y = [math.exp(0.5 * r[0] + rng.gauss(0.0, 0.1)) for r in X]
    P = BoxCoxProfile(y, X)
    assert not P.spans_one
    for lam in [-0.7, 0.0, 0.6, 1.0]:
        assert abs(P.loglik(lam) - _brute_loglik(y, X, lam)) < 1e-8 * (1.0 + abs(P.loglik(lam)))


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        box_cox_fit([1.0, 0.0, 2.0, 3.0])
    with pytest.raises(ValueError):
        box_cox_fit([1.0, -2.0, 2.0, 3.0])
    with pytest.raises(ValueError):
        box_cox([1.0, -1.0], 0.5)
    with pytest.raises(ValueError):
        box_cox_fit([1.0, 2.0, 3.0, 4.0], [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0]])
    with pytest.raises(ValueError):
        box_cox_fit([1.0, 2.0], [[1.0, 1.0], [1.0, 2.0]])


def test_open_interval_is_reported() -> None:
    # Two-point-like data give a flat profile: the interval runs past [lo, hi].
    lam, lmax, a, b = box_cox_fit([1.0, 1.1, 1.05, 1.08], lo=-0.5, hi=0.5)
    assert a is None and b is None
    assert -0.5 <= lam <= 0.5


def test_coverage_monte_carlo() -> None:
    rng = random.Random(21)
    n, r = 20, 200
    x = [1.0 + 9.0 * i / (n - 1) for i in range(n)]
    X = [[1.0, v] for v in x]
    cover = 0
    for _ in range(r):
        y = [math.exp(1.0 + 0.3 * v + rng.gauss(0.0, 0.25)) for v in x]
        _, _, a, b = box_cox_fit(y, X, lo=-3.0, hi=3.0)
        if (a is None or a <= 0.0) and (b is None or 0.0 <= b):
            cover += 1
    assert 0.88 <= cover / r <= 0.99
