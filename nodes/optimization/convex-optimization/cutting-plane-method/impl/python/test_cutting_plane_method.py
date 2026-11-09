# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cutting-plane-method/. The authors are listed in prov/6QC9VJ.jsonl.

import itertools
import math
import random
from fractions import Fraction

from cutting_plane_method import kelley, simplex_max


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


def gauss(m, r):
    k = len(r)
    t = [list(row) + [r[i]] for i, row in enumerate(m)]
    for col in range(k):
        piv = next((i for i in range(col, k) if t[i][col] != 0), None)
        if piv is None:
            return None
        t[col], t[piv] = t[piv], t[col]
        for i in range(k):
            if i != col and t[i][col] != 0:
                f = t[i][col] / t[col][col]
                t[i] = [p - f * q for p, q in zip(t[i], t[col])]
    return [t[i][k] / t[i][i] for i in range(k)]


def pwl_minimum(a, b, lo, hi):
    """min over the box of max_i a_i^T x + b_i, by enumeration of the vertices of {(x, t)}."""
    n = len(lo)
    rows = [(list(ai) + [Fraction(-1)], -bi) for ai, bi in zip(a, b)]  # a_i^T x - t <= -b_i
    for j in range(n):
        e = [Fraction(1) if i == j else Fraction(0) for i in range(n)]
        rows.append(([-v for v in e] + [Fraction(0)], -lo[j]))
        rows.append((e + [Fraction(0)], hi[j]))
    best = None
    for sub in itertools.combinations(rows, n + 1):
        p = gauss([r for r, _ in sub], [h for _, h in sub])
        if p is None or any(dot(r, p) > h for r, h in rows):
            continue
        if best is None or p[n] < best:
            best = p[n]
    return best


def check_history(res, fstar):
    prev_u = prev_l = None
    for j, (x, fx, g, u, low, xn) in enumerate(res.history):
        assert low <= fstar <= u  # the certified bounds
        if prev_u is not None:
            assert u <= prev_u and low >= prev_l
        prev_u, prev_l = u, low
        # each earlier point is far from the new point unless the gap is small
        for xi, fi, gi, _, _, _ in res.history[: j + 1]:
            d = [p - q for p, q in zip(xn, xi)]
            assert fi - low <= -dot(gi, d)
            assert (u - low) ** 2 <= dot(gi, gi) * dot(d, d)


def test_page_example() -> None:
    oracle = lambda x: (x[0] ** 2, [2 * x[0]])
    res = kelley(oracle, [Fraction(-1)], [Fraction(2)], [Fraction(2)], max_iter=6)
    expect = [  # x_j, f_j, U_j, L_j, x_{j+1}
        (2, 4, 4, -8, -1),
        (-1, 1, 1, -2, Fraction(1, 2)),
        (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), Fraction(-1, 2), Fraction(-1, 4)),
        (Fraction(-1, 4), Fraction(1, 16), Fraction(1, 16), Fraction(-1, 8), Fraction(1, 8)),
        (Fraction(1, 8), Fraction(1, 64), Fraction(1, 64), Fraction(-1, 32), Fraction(-1, 16)),
    ]
    for (x, fx, g, u, low, xn), (ex, ef, eu, el, exn) in zip(res.history, expect):
        assert (x, fx, u, low, xn) == ([ex], ef, eu, el, [exn])
    for j, (_, _, _, u, low, _) in enumerate(res.history[1:], start=1):
        assert u - low == 3 * Fraction(4) ** (1 - j)
    check_history(res, 0)


def test_random_piecewise_linear() -> None:
    rng = random.Random(9)
    for _ in range(500):
        n = rng.randint(1, 2)
        m = rng.randint(1, 4)
        a = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(m)]
        b = [Fraction(rng.randint(-3, 3)) for _ in range(m)]
        lo = [Fraction(rng.randint(-2, 0)) for _ in range(n)]
        hi = [v + rng.randint(1, 3) for v in lo]

        def oracle(x):
            vals = [dot(ai, x) + bi for ai, bi in zip(a, b)]
            i = vals.index(max(vals))
            return vals[i], a[i]

        fstar = pwl_minimum(a, b, lo, hi)
        x0 = [Fraction(rng.randint(int(l), int(h))) for l, h in zip(lo, hi)]
        res = kelley(oracle, lo, hi, x0, max_iter=m + 2)
        # each step either adds a new piece or closes the gap, so at most m + 1 oracle calls
        assert len(res.history) <= m + 1
        assert res.upper == res.lower == fstar
        check_history(res, fstar)


def test_random_quadratic() -> None:
    rng = random.Random(10)
    for _ in range(300):
        n = rng.randint(1, 2)
        c = [Fraction(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(n)]
        lo = [Fraction(rng.randint(-2, 0)) for _ in range(n)]
        hi = [v + rng.randint(1, 3) for v in lo]
        oracle = lambda x: (sum((p - q) ** 2 for p, q in zip(x, c)), [2 * (p - q) for p, q in zip(x, c)])
        fstar = sum((min(max(q, l), h) - q) ** 2 for q, l, h in zip(c, lo, hi))
        x0 = [Fraction(rng.randint(int(l), int(h))) for l, h in zip(lo, hi)]
        res = kelley(oracle, lo, hi, x0, max_iter=7)
        check_history(res, fstar)


def test_simplex_small() -> None:
    # maximize 3 v1 + 2 v2 subject to v1 + v2 <= 4, v1 + 3 v2 <= 6, v1 <= 3: optimum (3, 1), value 11
    a = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(3)], [Fraction(1), Fraction(0)]]
    v, val = simplex_max(a, [Fraction(4), Fraction(6), Fraction(3)], [Fraction(3), Fraction(2)])
    assert v == [3, 1] and val == 11


def test_eigenvalue_float() -> None:
    # f(x) = lambda_max([[2 + x1, x2], [x2, -x1]]) = 1 + sqrt((1 + x1)^2 + x2^2); f* = 1 at (-1, 0)
    def oracle(x):
        x1, x2 = float(x[0]), float(x[1])
        r = math.hypot(1 + x1, x2)
        g = [(1 + x1) / r, x2 / r] if r > 0 else [0.0, 0.0]
        return 1 + r, g

    res = kelley(oracle, [-2, -2], [2, 2], [2, 2], eps=1e-3, max_iter=200)
    assert res.upper - res.lower <= 1e-3
    assert res.lower <= 1 + 1e-12 <= res.upper + 2e-12
    assert math.hypot(float(res.x[0]) + 1, float(res.x[1])) <= 1e-3 + 1e-12
