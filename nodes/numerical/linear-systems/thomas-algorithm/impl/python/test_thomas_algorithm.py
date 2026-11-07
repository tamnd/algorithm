# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thomas-algorithm/. The authors are listed in prov/V8X0CR.jsonl.

import random
from fractions import Fraction

import pytest

from thomas_algorithm import ZeroPivot, thomas, thomas_cyclic, thomas_factor

U = Fraction(1, 2**53)
F_U = 4 * U + 3 * U**2 + U**3  # Higham, Section 9.6: the constant for the tridiagonal LU solve


def dense(a, b, c, alpha=0, beta=0):
    n = len(b)
    m = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = Fraction(b[i])
        if i > 0:
            m[i][i - 1] = Fraction(a[i])
        if i < n - 1:
            m[i][i + 1] = Fraction(c[i])
    if n > 1:
        m[0][n - 1] += Fraction(alpha)
        m[n - 1][0] += Fraction(beta)
    return m


def exact_solve(m, d):
    n = len(d)
    g = [list(row) + [Fraction(di)] for row, di in zip(m, d)]
    for k in range(n):
        p = next(i for i in range(k, n) if g[i][k] != 0)
        g[k], g[p] = g[p], g[k]
        piv = g[k][k]
        g[k] = [v / piv for v in g[k]]
        for i in range(n):
            if i != k and g[i][k] != 0:
                f = g[i][k]
                g[i] = [v - f * w for v, w in zip(g[i], g[k])]
    return [row[n] for row in g]


def random_system(rng, n, dominant=True):
    a = [rng.uniform(-1, 1) for _ in range(n)]
    c = [rng.uniform(-1, 1) for _ in range(n)]
    b = [rng.uniform(-1, 1) for _ in range(n)]
    if dominant:
        b = [(abs(a[i]) + abs(c[i]) + rng.uniform(0.01, 1)) * rng.choice((-1, 1)) for i in range(n)]
    d = [rng.uniform(-1, 1) for _ in range(n)]
    return a, b, c, d


def check_backward(a, b, c, d, x):
    """Exact check of |d - A x| <= f(u) |L||U| |x| (Higham, Section 9.6)."""
    n = len(b)
    l, u = thomas_factor(a, b, c)
    fx = [Fraction(v) for v in x]
    for i in range(n):
        r = Fraction(d[i]) - Fraction(b[i]) * fx[i]
        if i > 0:
            r -= Fraction(a[i]) * fx[i - 1]
        if i < n - 1:
            r -= Fraction(c[i]) * fx[i + 1]
        # row i of |L||U|: |l_i| |u_{i-1}| at i-1, |l_i| |c_{i-1}| + |u_i| at i, |c_i| at i+1
        s = abs(Fraction(u[i])) * abs(fx[i])
        if i > 0:
            s += abs(Fraction(l[i])) * (abs(Fraction(u[i - 1])) * abs(fx[i - 1]) + abs(Fraction(c[i - 1])) * abs(fx[i]))
        if i < n - 1:
            s += abs(Fraction(c[i])) * abs(fx[i + 1])
        assert abs(r) <= F_U * s


def test_exact_example():
    a = [0, -1, -1, -1]
    b = [2, 2, 2, 2]
    c = [-1, -1, -1, 0]
    d = [1, 0, 0, 1]
    x = thomas([Fraction(v) for v in a], [Fraction(v) for v in b], [Fraction(v) for v in c], [Fraction(v) for v in d])
    assert x == [1, 1, 1, 1]
    l, u = thomas_factor([Fraction(v) for v in a], [Fraction(v) for v in b], [Fraction(v) for v in c])
    assert u == [2, Fraction(3, 2), Fraction(4, 3), Fraction(5, 4)]


def test_random_diagonally_dominant():
    for seed in range(60):
        rng = random.Random(seed)
        n = rng.randint(1, 40)
        a, b, c, d = random_system(rng, n)
        x = thomas(a, b, c, d)
        check_backward(a, b, c, d, x)
        # exact reference: the same elimination in rational arithmetic, checked against dense elimination for small n
        ex = thomas(*[[Fraction(v) for v in t] for t in (a, b, c, d)])
        if n <= 6:
            assert ex == exact_solve(dense(a, b, c), d)
        # diagonal dominance: kappa_inf is modest, so the forward error is small (observed)
        err = max(abs(Fraction(xi) - e) for xi, e in zip(x, ex)) / max(abs(e) for e in ex)
        assert err < 1e-12, seed


def test_random_general_meets_componentwise_bound():
    for seed in range(40):
        rng = random.Random(500 + seed)
        n = rng.randint(2, 30)
        a, b, c, d = random_system(rng, n, dominant=False)
        try:
            x = thomas(a, b, c, d)
        except ZeroPivot:
            continue
        check_backward(a, b, c, d, x)


def test_spd_model_problem_large():
    n = 2000
    a = [-1.0] * n
    b = [2.0] * n
    c = [-1.0] * n
    xs = [((i * 7) % 13) / 13.0 for i in range(n)]
    d = [2 * xs[i] - (xs[i - 1] if i > 0 else 0) - (xs[i + 1] if i < n - 1 else 0) for i in range(n)]
    x = thomas(a, b, c, d)
    # kappa_2(T_n) is about 4 (n + 1)^2 / pi^2, near 1.6e6
    assert max(abs(x[i] - xs[i]) for i in range(n)) < 1e-8


def test_one_by_one_and_diagonal():
    assert thomas([0.0], [4.0], [0.0], [2.0]) == [0.5]
    assert thomas([0.0, 0.0, 0.0], [1.0, 2.0, 4.0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]) == [1.0, 0.5, 0.25]


def test_triangular_bidiagonal():
    # lower bidiagonal: c = 0, so U is diagonal and the method is forward substitution
    x = thomas([0.0, 1.0, 1.0], [1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [1.0, 2.0, 3.0])
    assert x == [1.0, 1.0, 2.0]


def test_zero_pivot_needs_a_swap():
    with pytest.raises(ZeroPivot):
        thomas([0.0, 1.0], [0.0, 1.0], [1.0, 0.0], [1.0, 2.0])


def test_singular_is_reported():
    # [[1, 1], [1, 1]]: the second pivot is 0
    with pytest.raises(ZeroPivot):
        thomas([0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [1.0, 1.0])


def test_tiny_pivot_loses_accuracy_without_pivoting():
    e = 1e-17
    x = thomas([0.0, 1.0], [e, 1.0], [1.0, 0.0], [1.0, 2.0])
    ex = exact_solve(dense([0, 1], [e, 1], [1, 0]), [1, 2])
    assert abs(x[0] - float(ex[0])) > 0.5  # x_1 is about 1 but is computed as 0
    check_backward([0.0, 1.0], [e, 1.0], [1.0, 0.0], [1.0, 2.0], x)  # the bound still holds: |L||U| is huge


def test_cyclic_matches_exact():
    for seed in range(20):
        rng = random.Random(900 + seed)
        n = rng.randint(3, 15)
        a, b, c, d = random_system(rng, n)
        alpha, beta = rng.uniform(-0.005, 0.005), rng.uniform(-0.005, 0.005)
        b = [bi + (0.01 if bi > 0 else -0.01) for bi in b]
        x = thomas_cyclic(a, b, c, d, alpha, beta)
        ex = exact_solve(dense(a, b, c, alpha, beta), d)
        err = max(abs(Fraction(xi) - e) for xi, e in zip(x, ex)) / max(abs(e) for e in ex)
        assert err < 1e-11, seed
