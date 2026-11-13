# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rls-algorithm/. The authors are listed in prov/BJHGVT.jsonl.

import random
from fractions import Fraction as F

import pytest

from rls_algorithm import rls, rls_update


def solve(a, b):
    """Gauss-Jordan elimination, first nonzero pivot; exact on Fraction."""
    n = len(a)
    m = [list(row) + [bb] for row, bb in zip(a, b)]
    for c in range(n):
        piv = max(range(c, n), key=lambda i: abs(m[i][c]))
        m[c], m[piv] = m[piv], m[c]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [u - f * v for u, v in zip(m[i], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def batch(x, d, m, lam, delta, n):
    """Weighted, regularized least squares on the samples 0..n, by the normal equations."""
    zero = 0 * delta
    us = [[x[i - k] if i - k >= 0 else zero for k in range(m)] for i in range(n + 1)]
    phi = [[lam ** (n + 1) * delta * (1 if i == j else 0) for j in range(m)] for i in range(m)]
    z = [zero] * m
    for i, u in enumerate(us):
        g = lam ** (n - i)
        for a in range(m):
            z[a] += g * d[i] * u[a]
            for b in range(m):
                phi[a][b] += g * u[a] * u[b]
    return solve(phi, z), phi


def test_trace_on_the_page() -> None:
    x = [F(1), F(-1), F(2), F(0), F(1), F(-2)]
    d = [F(1), F(-1, 2), F(3, 2), F(1), F(1), F(-3, 2)]
    want = [(F(1, 2), 0), (F(1, 2), 0), (F(5, 8), F(-1, 24)), (F(63, 80), F(27, 80)),
            (F(77, 94), F(33, 94)), (F(121, 142), F(49, 142))]
    for n in range(6):
        w, p, _ = rls(x[:n + 1], d[:n + 1], 2, F(1), F(1))
        assert tuple(w) == want[n]
    assert p == [[F(8, 71), F(5, 71)], [F(5, 71), F(12, 71)]]


def test_equals_regularized_batch_least_squares_in_fractions() -> None:
    rng = random.Random(5401)
    for case in range(500):
        m = rng.randint(1, 4)
        n_samples = rng.randint(1, 9)
        x = [F(rng.randint(-5, 5)) for _ in range(n_samples)]
        d = [F(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(n_samples)]
        lam = F(1) if case % 2 == 0 else F(rng.randint(1, 10), 10)
        delta = F(rng.randint(1, 20), rng.randint(1, 20))
        w, p, _ = rls(x, d, m, lam, delta)
        want, phi = batch(x, d, m, lam, delta, n_samples - 1)
        assert w == want
        prod = [[sum(p[i][k] * phi[k][j] for k in range(m)) for j in range(m)] for i in range(m)]
        assert prod == [[1 if i == j else 0 for j in range(m)] for i in range(m)]  # P = Phi^-1


def test_float_lambda_one_matches_batch_to_1e9() -> None:
    rng = random.Random(5402)
    h = [0.7, -0.3, 0.2, 0.1]
    x = [rng.gauss(0, 1) for _ in range(300)]
    d = [sum(h[k] * x[n - k] for k in range(4) if n - k >= 0) + rng.gauss(0, 0.1) for n in range(300)]
    for delta in (0.01, 1.0, 100.0):
        w, _, _ = rls(x, d, 4, 1.0, delta)
        want, _ = batch(x, d, 4, 1.0, delta, 299)
        assert max(abs(a - b) for a, b in zip(w, want)) < 1e-9


def test_a_posteriori_error_and_gain() -> None:
    """e+ = xi * lam / (lam + u^T P u), and k = P_new u."""
    rng = random.Random(5403)
    for _ in range(500):
        m = rng.randint(1, 3)
        a = [[F(rng.randint(-3, 3)) for _ in range(m)] for _ in range(m)]
        p = [[sum(a[k][i] * a[k][j] for k in range(m)) + (1 if i == j else 0) for j in range(m)] for i in range(m)]
        w = [F(rng.randint(-3, 3)) for _ in range(m)]
        u = [F(rng.randint(-3, 3)) for _ in range(m)]
        d, lam = F(rng.randint(-5, 5)), F(rng.randint(1, 4), 4)
        w2, p2, xi = rls_update(w, p, u, d, lam)
        q = sum(u[i] * sum(p[i][j] * u[j] for j in range(m)) for i in range(m))
        assert d - sum(a * b for a, b in zip(w2, u)) == xi * lam / (lam + q)
        k = [(w2[i] - w[i]) / xi for i in range(m)] if xi != 0 else None
        if k is not None:
            assert k == [sum(p2[i][j] * u[j] for j in range(m)) for i in range(m)]


def test_tracks_a_change_with_forgetting() -> None:
    rng = random.Random(5404)
    x = [rng.gauss(0, 1) for _ in range(800)]
    h1, h2 = [1.0, 0.5], [-0.5, 0.25]
    d = [sum((h1 if n < 400 else h2)[k] * x[n - k] for k in range(2) if n - k >= 0) for n in range(800)]
    w, _, _ = rls(x, d, 2, 0.95, 1.0)
    assert max(abs(a - b) for a, b in zip(w, h2)) < 1e-6
    w, _, _ = rls(x, d, 2, 1.0, 1.0)  # no forgetting: stuck between the two systems
    assert max(abs(a - b) for a, b in zip(w, h2)) > 0.3


def test_errors() -> None:
    with pytest.raises(ValueError):
        rls([1], [1], 1, 1.5, 1.0)
    with pytest.raises(ValueError):
        rls([1], [1], 1, 1.0, 0.0)
    with pytest.raises(ValueError):
        rls([1, 2], [1], 1, 1.0, 1.0)
