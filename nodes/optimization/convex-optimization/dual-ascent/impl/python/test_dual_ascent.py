# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-ascent/. The authors are listed in prov/CHE5ZR.jsonl.

import itertools
import random
from fractions import Fraction

from dual_ascent import dual_ascent, quadratic_argmin, solve


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


def kkt_oracle(q, c, a, b, ineq):
    """Exact x*, y* by enumeration of active sets. Returns None if no nonsingular active set works."""
    n, m = len(c), len(b)
    eq = [i for i in range(m) if not ineq[i]]
    iq = [i for i in range(m) if ineq[i]]
    for size in range(len(iq) + 1):
        for s in itertools.combinations(iq, size):
            w = eq + list(s)
            mat = [q[i] + [a[k][i] for k in w] for i in range(n)] + [a[k] + [Fraction(0)] * len(w) for k in w]
            try:
                sol = solve(mat, [-ci for ci in c] + [b[k] for k in w])
            except ValueError:
                continue
            x, yw = sol[:n], sol[n:]
            if any(dot(a[i], x) > b[i] for i in iq) or any(yw[j] < 0 for j, k in enumerate(w) if ineq[k]):
                continue
            y = [Fraction(0)] * m
            for j, k in enumerate(w):
                y[k] = yw[j]
            return x, y
    return None


def check_run(res, q, c, a, b, ineq, alpha, mu, xstar, ystar):
    f = lambda x: dot(x, [dot(row, x) for row in q]) / 2 + dot(c, x)
    fstar = f(xstar)
    # strong duality at the oracle pair
    assert all(dot(q[i], xstar) + c[i] + sum(a[k][i] * ystar[k] for k in range(len(b))) == 0 for i in range(len(c)))
    y0 = res.steps[0][0]
    r0 = dot([u - v for u, v in zip(y0, ystar)], [u - v for u, v in zip(y0, ystar)])
    prev = None
    for k, (y, x, g) in enumerate(res.steps):
        assert all(yi >= 0 for yi, t in zip(y, ineq) if t)
        dual = f(x) + dot(y, g)  # = d(y_k), since x = x(y_k)
        assert dual <= fstar  # weak duality
        if k >= 1:
            assert fstar - dual <= r0 / (2 * alpha * k)
            assert dot([u - v for u, v in zip(x, xstar)], [u - v for u, v in zip(x, xstar)]) <= 2 * (fstar - dual) / mu
            assert dual >= prev  # the dual value does not decrease
        prev = dual


def test_page_example() -> None:
    # minimize x1^2 / 2 + x2^2 subject to x1 + x2 = 3; x* = (2, 1), y* = -2, f* = 3
    q = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(2)]]
    c, a, b, ineq = [Fraction(0), Fraction(0)], [[Fraction(1), Fraction(1)]], [Fraction(3)], [False]
    alpha = Fraction(1, 2)  # mu / ||A||_F^2 = 1 / 2
    res = dual_ascent(quadratic_argmin(q, c, a), a, b, ineq, [Fraction(0)], alpha, max_iter=7)
    for k, (y, x, g) in enumerate(res.steps):
        e = Fraction(1, 4**k)
        assert y == [-2 + 2 * e]
        assert x == [2 - 2 * e, 1 - e]
        assert g == [-3 * e]
        assert x[0] ** 2 / 2 + x[1] ** 2 + y[0] * g[0] == 3 * (1 - e * e)
    check_run(res, q, c, a, b, ineq, alpha, Fraction(1), [Fraction(2), Fraction(1)], [Fraction(-2)])


def test_random_qp() -> None:
    rng = random.Random(7)
    done = 0
    while done < 500:
        n = rng.randint(1, 3)
        m = rng.randint(1, 3)
        mu = Fraction(rng.choice([1, 2]), rng.choice([1, 2]))
        rows = [[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(rng.randint(0, n))]
        q = [[sum(r[i] * r[j] for r in rows) + (mu if i == j else 0) for j in range(n)] for i in range(n)]
        c = [Fraction(rng.randint(-4, 4)) for _ in range(n)]
        a = [[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(m)]
        ineq = [rng.random() < 0.6 for _ in range(m)]
        x0 = [Fraction(rng.randint(-2, 2)) for _ in range(n)]
        b = [dot(a[i], x0) + (rng.randint(0, 2) if ineq[i] else 0) for i in range(m)]
        frob = sum(v * v for row in a for v in row)
        if frob == 0:
            continue
        sol = kkt_oracle(q, c, a, b, ineq)
        if sol is None:
            continue  # dependent active rows; the oracle cannot find a unique multiplier
        xstar, ystar = sol
        alpha = mu / frob
        y0 = [Fraction(rng.randint(0 if t else -2, 2)) for t in ineq]
        res = dual_ascent(quadratic_argmin(q, c, a), a, b, ineq, y0, alpha, max_iter=8)
        check_run(res, q, c, a, b, ineq, alpha, mu, xstar, ystar)
        done += 1


def test_float_stop_rule() -> None:
    # minimize ||x||^2 / 2 - x1 - x2 subject to x1 + 2 x2 <= 1 and x1 - x2 = 0; x* = (1/3, 1/3), y* = (4/9, 2/9)
    q = [[1.0, 0.0], [0.0, 1.0]]
    c = [-1.0, -1.0]
    a, b, ineq = [[1.0, 2.0], [1.0, -1.0]], [1.0, 0.0], [True, False]
    res = dual_ascent(quadratic_argmin(q, c, a), a, b, ineq, [0.0, 0.0], 1.0 / 7.0, eps=1e-10)
    assert len(res.steps) < 1000
    assert all(abs(u - v) < 1e-9 for u, v in zip(res.x, [1 / 3, 1 / 3]))
    assert all(abs(u - v) < 1e-9 for u, v in zip(res.y, [4 / 9, 2 / 9]))
