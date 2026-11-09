# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proximal-point-method/. The authors are listed in prov/V8N3PJ.jsonl.

import random
from fractions import Fraction

from proximal_point_method import prox_box_linear, prox_l1, prox_quadratic, proximal_point_method


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def sub(u, v):
    return [a - b for a, b in zip(u, v)]


def check_run(res, f, fstar, xstar, lam):
    """The O(1/k) bound, monotone values, Fejer monotone distances, and the subgradient certificate."""
    d0 = dot(sub(res.iterates[0], xstar), sub(res.iterates[0], xstar))
    for k in range(1, len(res.iterates)):
        xk, xprev = res.iterates[k], res.iterates[k - 1]
        gap = f(xk) - fstar
        assert 0 <= gap <= d0 / (2 * lam * k)
        assert f(xk) <= f(xprev)
        assert dot(sub(xk, xstar), sub(xk, xstar)) <= dot(sub(xprev, xstar), sub(xprev, xstar))
        g = res.subgradients[k - 1]
        # g is a subgradient at x_k, so f* >= f(x_k) + g^T (x* - x_k): the gap is certified
        assert gap <= dot(g, sub(xk, xstar))


def rand_frac(rng, lo, hi):
    return Fraction(rng.randint(lo * 4, hi * 4), 4)


def test_page_example() -> None:
    q = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(10)]]
    c = [Fraction(0), Fraction(0)]
    f = lambda x: (x[0] ** 2 + 10 * x[1] ** 2) / 2
    res = proximal_point_method(prox_quadratic(q, c), [Fraction(1), Fraction(1)], Fraction(1), max_iter=5)
    for k, x in enumerate(res.iterates):
        assert x == [Fraction(1, 2**k), Fraction(1, 11**k)]
    assert res.iterates[1] == [Fraction(1, 2), Fraction(1, 11)]
    assert f(res.iterates[1]) == Fraction(1, 8) + Fraction(5, 121)
    check_run(res, f, 0, [0, 0], Fraction(1))


def test_quadratic_exact() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 3)
        mrows = [[Fraction(rng.randint(-2, 2)) for _ in range(n)] for _ in range(rng.randint(1, 3))]
        q = [[sum(r[i] * r[j] for r in mrows) for j in range(n)] for i in range(n)]  # Q = M^T M, maybe singular
        z = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        c = [-sum(q[i][j] * z[j] for j in range(n)) for i in range(n)]  # z minimizes, since Q z + c = 0
        f = lambda x, q=q, c=c: dot(x, [dot(row, x) for row in q]) / 2 + dot(c, x)
        lam = Fraction(rng.choice([1, 2, 4]), rng.choice([1, 2]))
        x0 = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        res = proximal_point_method(prox_quadratic(q, c), x0, lam, max_iter=12)
        check_run(res, f, f(z), z, lam)
        for k in range(1, len(res.iterates)):
            xk = res.iterates[k]
            assert res.subgradients[k - 1] == [dot(q[i], xk) + c[i] for i in range(n)]  # the gradient, exactly


def test_strongly_convex_rate() -> None:
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(1, 3)
        diag = [Fraction(rng.randint(1, 6)) for _ in range(n)]
        q = [[diag[i] if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        z = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        c = [-diag[i] * z[i] for i in range(n)]
        lam = Fraction(rng.randint(1, 4), 2)
        mu = min(diag)
        x0 = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        res = proximal_point_method(prox_quadratic(q, c), x0, lam, max_iter=10)
        d0 = dot(sub(x0, z), sub(x0, z))
        for k, x in enumerate(res.iterates):
            assert dot(sub(x, z), sub(x, z)) <= d0 / (1 + lam * mu) ** (2 * k)


def test_l1_finite() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 4)
        a = [rand_frac(rng, -3, 3) for _ in range(n)]
        f = lambda x, a=a: sum(abs(u - v) for u, v in zip(x, a))
        lam = Fraction(rng.randint(1, 6), 4)
        x0 = [rand_frac(rng, -6, 6) for _ in range(n)]
        res = proximal_point_method(prox_l1(a), x0, lam, max_iter=200)
        # f is polyhedral: the method reaches the minimizer a in ceil(max |x0_i - a_i| / lam) steps
        steps = max(-((-abs(u - v)) // lam) for u, v in zip(x0, a))
        assert res.iterates[int(steps)] == a
        check_run(res, f, 0, a, lam)


def test_box_lp() -> None:
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(1, 4)
        lo = [rand_frac(rng, -3, 0) for _ in range(n)]
        hi = [l + rand_frac(rng, 0, 3) for l in lo]
        c = [rand_frac(rng, -2, 2) for _ in range(n)]
        f = lambda x, c=c: dot(c, x)
        # independent oracle: a linear function on a box is minimized coordinate by coordinate
        xstar = [l if ci > 0 else u for ci, l, u in zip(c, lo, hi)]
        fstar = sum(min(ci * l, ci * u) for ci, l, u in zip(c, lo, hi))
        assert f(xstar) == fstar
        lam = Fraction(rng.randint(1, 4), 2)
        x0 = [l + (u - l) * Fraction(rng.randint(0, 4), 4) for l, u in zip(lo, hi)]
        res = proximal_point_method(prox_box_linear(c, lo, hi), x0, lam, max_iter=100)
        assert f(res.x) == fstar  # finite termination on a polyhedral function
        check_run(res, f, fstar, xstar, lam)


def test_float_stop_rule() -> None:
    q = [[2.0, 1.0], [1.0, 2.0]]
    c = [-1.0, 1.0]
    res = proximal_point_method(prox_quadratic(q, c), [3.0, -4.0], 0.5, eps=1e-10, max_iter=10000)
    g = res.subgradients[-1]
    assert sum(v * v for v in g) <= 1e-20
    assert abs(res.x[0] - 1.0) < 1e-9 and abs(res.x[1] + 1.0) < 1e-9
