# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/augmented-lagrangian-method/. The authors are listed in prov/27GRBM.jsonl.

import random
from fractions import Fraction

from augmented_lagrangian_method import augmented_lagrangian_method, quadratic_argmin, solve


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


def kkt(q, c, a, b):
    """Exact solution of [Q A^T; A 0] [x; y] = [-c; b], or None if the KKT matrix is singular."""
    n, m = len(c), len(b)
    mat = [q[i] + [a[k][i] for k in range(m)] for i in range(n)] + [a[k] + [Fraction(0)] * m for k in range(m)]
    try:
        sol = solve(mat, [-ci for ci in c] + list(b))
    except ValueError:
        return None
    return sol[:n], sol[n:]


def check_run(res, q, c, a, b, y0, rho, xstar, ystar):
    f = lambda x: dot(x, [dot(row, x) for row in q]) / 2 + dot(c, x)
    fstar = f(xstar)
    d0 = dot([u - v for u, v in zip(y0, ystar)], [u - v for u, v in zip(y0, ystar)])
    prev = None
    for k, (x, y, r) in enumerate(res.steps, start=1):
        # x_k minimizes the ordinary Lagrangian at y_k: Q x + c + A^T y = 0, exactly
        grad = [dot(q[i], x) + c[i] + sum(a[j][i] * y[j] for j in range(len(b))) for i in range(len(c))]
        assert all(v == 0 for v in grad)
        dual = f(x) + dot(y, r)  # = d(y_k)
        assert dual <= fstar  # weak duality
        assert fstar - dual <= d0 / (2 * rho * k)
        assert dot(r, r) <= d0 / (rho * rho * k)
        assert f(x) - dual == -dot(y, r)  # the duality gap, known after each step
        if prev is not None:
            assert dot(r, r) <= dot(prev, prev)
        prev = r


def test_page_example() -> None:
    q, c, a, b = [[Fraction(1)]], [Fraction(0)], [[Fraction(1)]], [Fraction(1)]
    res = augmented_lagrangian_method(quadratic_argmin(q, c, a, b), a, b, [Fraction(0)], Fraction(1), max_iter=6)
    for k, (x, y, r) in enumerate(res.steps, start=1):
        assert x == [1 - Fraction(1, 2**k)]
        assert y == [-1 + Fraction(1, 2**k)]
        assert x[0] ** 2 / 2 + y[0] * r[0] == (1 - Fraction(1, 4**k)) / 2
    check_run(res, q, c, a, b, [Fraction(0)], Fraction(1), [Fraction(1)], [Fraction(-1)])


def test_random_qp() -> None:
    rng = random.Random(5)
    done = 0
    while done < 500:
        n = rng.randint(1, 4)
        m = rng.randint(1, n)
        rows = [[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(rng.randint(0, n))]
        q = [[sum(r[i] * r[j] for r in rows) for j in range(n)] for i in range(n)]  # PSD, often singular
        c = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        a = [[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(m)]
        b = [Fraction(rng.randint(-3, 3)) for _ in range(m)]
        sol = kkt(q, c, a, b)
        if sol is None:
            continue  # A rank deficient, or Q singular on the null space of A
        xstar, ystar = sol
        rho = Fraction(rng.choice([1, 2, 4]), rng.choice([1, 2]))
        y0 = [Fraction(rng.randint(-2, 2)) for _ in range(m)]
        res = augmented_lagrangian_method(quadratic_argmin(q, c, a, b), a, b, y0, rho, max_iter=8)
        check_run(res, q, c, a, b, y0, rho, xstar, ystar)
        done += 1


def test_float_stop_rule() -> None:
    q = [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]]
    c = [0.0, 0.0, 0.0]
    a, b = [[1.0, 1.0, 1.0]], [1.0]
    res = augmented_lagrangian_method(quadratic_argmin(q, c, a, b), a, b, [0.0], 10.0, eps=1e-12)
    assert len(res.steps) < 20
    assert all(abs(u - v) < 1e-10 for u, v in zip(res.x, [6 / 11, 3 / 11, 2 / 11]))
    assert abs(res.y[0] + 6 / 11) < 1e-10
