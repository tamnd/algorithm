# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-casteljau-algorithm/. The authors are listed in prov/MPYB8D.jsonl.

import random
from fractions import Fraction
from math import comb

from de_casteljau_algorithm import (
    de_casteljau,
    evaluate,
    evaluate_with_derivative,
    rational_de_casteljau,
    subdivide,
)

F = Fraction


def bernstein_sum(points, t):
    """The reference: sum of P_i C(n, i) t^i (1 - t)^(n - i)."""
    n = len(points) - 1
    dim = len(points[0])
    return tuple(sum(p[k] * comb(n, i) * t**i * (1 - t) ** (n - i) for i, p in enumerate(points)) for k in range(dim))


def random_points(rng, n, dim=2, size=20):
    return [tuple(F(rng.randint(-size, size), rng.randint(1, 4)) for _ in range(dim)) for _ in range(n + 1)]


def random_t(rng):
    q = rng.randint(1, 30)
    return F(rng.randint(0, q), q)


def test_example() -> None:
    P = [(0, 0), (1, 2), (3, 2), (4, 0)]
    assert evaluate(P, F(1, 2)) == (2, F(3, 2))
    assert evaluate_with_derivative(P, F(1, 4)) == ((F(29, 32), F(9, 8)), (F(33, 8), 3))
    left, right = subdivide(P, F(1, 2))
    assert left == [(0, 0), (F(1, 2), 1), (F(5, 4), F(3, 2)), (2, F(3, 2))]
    assert right == [(2, F(3, 2)), (F(11, 4), F(3, 2)), (F(7, 2), 1), (4, 0)]


def test_against_bernstein_sum() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 9)
        P = random_points(rng, n, dim=rng.randint(1, 3))
        t = random_t(rng)
        assert evaluate(P, t) == bernstein_sum(P, t)
    # also outside [0, 1], where the same polynomial is extrapolated
    P = random_points(rng, 5)
    for t in (F(-3, 2), F(7, 3)):
        assert evaluate(P, t) == bernstein_sum(P, t)


def test_subdivision_halves() -> None:
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(0, 7)
        P = random_points(rng, n)
        t = random_t(rng)
        point, left, right = de_casteljau(P, t)
        assert left[0] == tuple(P[0]) and right[-1] == tuple(P[-1])
        assert left[-1] == right[0] == point
        for _ in range(4):
            u = random_t(rng)
            assert bernstein_sum(left, u) == bernstein_sum(P, t * u)
            assert bernstein_sum(right, u) == bernstein_sum(P, t + (1 - t) * u)


def test_derivative() -> None:
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(1, 8)
        P = random_points(rng, n)
        t = random_t(rng)
        # B'(t) = n sum (P_{i+1} - P_i) B_i^{n-1}(t)
        D = [tuple(n * (b - a) for a, b in zip(P[i], P[i + 1])) for i in range(n)]
        point, deriv = evaluate_with_derivative(P, t)
        assert point == bernstein_sum(P, t)
        assert deriv == bernstein_sum(D, t)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def hull(points):
    """Andrew's monotone chain, counterclockwise, without collinear points."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def in_hull(h, q):
    if len(h) == 1:
        return q == h[0]
    if len(h) == 2:
        a, b = h
        return orient(a, b, q) == 0 and min(a, b) <= q <= max(a, b)
    return all(orient(h[i], h[(i + 1) % len(h)], q) >= 0 for i in range(len(h)))


def test_convex_hull_property() -> None:
    rng = random.Random(4)
    for _ in range(120):
        n = rng.randint(0, 7)
        P = random_points(rng, n, size=6)
        h = hull(P)
        for _ in range(8):
            assert in_hull(h, evaluate(P, random_t(rng)))
        # the sub-polygons of a split lie in the hull of the original polygon
        left, right = subdivide(P, random_t(rng))
        assert all(in_hull(h, q) for q in left + right)
    # outside [0, 1] the property fails
    P = [(0, 0), (1, 2), (2, 0)]
    assert not in_hull(hull(P), evaluate(P, F(2)))


def sign_changes(seq):
    s = [x for x in seq if x != 0]
    return sum(1 for a, b in zip(s, s[1:]) if (a > 0) != (b > 0))


def bernstein_to_power(c):
    n = len(c) - 1
    p = [F(0)] * (n + 1)
    for i, ci in enumerate(c):
        for k in range(i, n + 1):
            p[k] += ci * (-1) ** (k - i) * comb(n, k) * comb(k, i)
    while p and p[-1] == 0:
        p.pop()
    return p


def peval(p, t):
    r = F(0)
    for a in reversed(p):
        r = r * t + a
    return r


def sturm_roots_open_unit(p):
    """Number of distinct real roots of p in (0, 1), by Sturm's theorem."""
    def rem(a, b):
        a = list(a)
        while len(a) >= len(b) and a:
            k = a[-1] / b[-1]
            s = len(a) - len(b)
            for i, x in enumerate(b):
                a[s + i] -= k * x
            while a and a[-1] == 0:
                a.pop()
        return a

    d = [i * a for i, a in enumerate(p)][1:]
    chain = [p, d]
    while True:
        r = rem(chain[-2], chain[-1])
        if not r:
            break
        chain.append([-x for x in r])

    def v(t):
        return sign_changes([peval(q, t) for q in chain])

    # roots in (0, 1] minus a root at 1
    return v(F(0)) - v(F(1)) - (1 if peval(p, F(1)) == 0 else 0)


def test_variation_diminishing() -> None:
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(1, 7)
        P = random_points(rng, n, size=8)
        # a random line a x + b y + c = 0
        a, b, c = F(rng.randint(-5, 5)), F(rng.randint(-5, 5)), F(rng.randint(-20, 20), 2)
        if a == 0 and b == 0:
            continue
        d = [a * x + b * y + c for x, y in P]
        if all(x == 0 for x in d):
            continue  # the curve lies on the line
        p = bernstein_to_power(d)
        if not p or len(p) == 1:
            continue
        crossings_curve = sturm_roots_open_unit(p)
        assert crossings_curve <= sign_changes(d)


def test_rational_quarter_circle() -> None:
    P = [(1, 0), (1, 1), (0, 1)]
    w = [1, 1, 2]
    assert rational_de_casteljau(P, w, F(1, 2)) == (F(3, 5), F(4, 5))
    rng = random.Random(6)
    for _ in range(100):
        t = random_t(rng)
        x, y = rational_de_casteljau(P, w, t)
        assert x * x + y * y == 1 and x >= 0 and y >= 0
        assert (x, y) == ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))


def test_rational_against_direct_ratio() -> None:
    rng = random.Random(7)
    for _ in range(100):
        n = rng.randint(0, 6)
        P = random_points(rng, n)
        w = [F(rng.randint(1, 9), rng.randint(1, 3)) for _ in range(n + 1)]
        t = random_t(rng)
        num = bernstein_sum([tuple(wi * x for x in p) for p, wi in zip(P, w)], t)
        den = bernstein_sum([(wi,) for wi in w], t)[0]
        assert rational_de_casteljau(P, w, t) == tuple(x / den for x in num)


def test_float_input() -> None:
    P = [(0.0, 0.0), (1.0, 2.0), (3.0, 2.0), (4.0, 0.0)]
    x, y = evaluate(P, 0.25)
    assert abs(x - 29 / 32) < 1e-12 and abs(y - 9 / 8) < 1e-12
