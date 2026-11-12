# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bezier-triangle/. The authors are listed in prov/6DPB5V.jsonl.

import random
from fractions import Fraction
from math import comb, factorial

import pytest

from bezier_triangle import (boundary_curve, de_casteljau_levels, directional_derivative,
                             from_function, indices, triangle_point)


def tri_bernstein(n, i, j, k, r, s, t):
    if min(i, j, k) < 0:
        return 0
    return Fraction(factorial(n), factorial(i) * factorial(j) * factorial(k)) * r ** i * s ** j * t ** k


def direct_sum(net, n, r, s, t):
    out = [0] * len(next(iter(net.values())))
    for (i, j, k), p in net.items():
        w = tri_bernstein(n, i, j, k, r, s, t)
        for a, x in enumerate(p):
            out[a] += w * x
    return tuple(out)


def direct_derivative(net, n, r, s, t, d):
    """Sum of P_ijk times the directional derivative of B_ijk, from the product rule."""
    out = [0] * len(next(iter(net.values())))
    for (i, j, k), p in net.items():
        w = n * (d[0] * tri_bernstein(n - 1, i - 1, j, k, r, s, t)
                 + d[1] * tri_bernstein(n - 1, i, j - 1, k, r, s, t)
                 + d[2] * tri_bernstein(n - 1, i, j, k - 1, r, s, t))
        for a, x in enumerate(p):
            out[a] += w * x
    return tuple(out)


def random_net(rng, n, dim=3):
    return {idx: tuple(Fraction(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(dim))
            for idx in indices(n)}


def random_bary(rng):
    a, b = sorted((rng.randint(0, 30), rng.randint(0, 30)))
    return Fraction(a, 30), Fraction(b - a, 30), Fraction(30 - b, 30)


def curve_sum(points, t):
    n = len(points) - 1
    return tuple(sum(comb(n, i) * t ** i * (1 - t) ** (n - i) * p[a] for i, p in enumerate(points))
                 for a in range(len(points[0])))


QUAD = {(2, 0, 0): (0, 0, 0), (0, 2, 0): (2, 0, 0), (0, 0, 2): (0, 2, 0),
        (1, 1, 0): (1, 0, 1), (0, 1, 1): (1, 1, 1), (1, 0, 1): (0, 1, 1)}


def test_worked_example():
    third = Fraction(1, 3)
    assert triangle_point(QUAD, third, third, third) == (Fraction(2, 3), Fraction(2, 3), Fraction(2, 3))
    lv = de_casteljau_levels(QUAD, third, third, third, stop=1)
    assert lv[(1, 0, 0)] == (Fraction(1, 3), Fraction(1, 3), Fraction(2, 3))
    assert lv[(0, 1, 0)] == (Fraction(4, 3), Fraction(1, 3), Fraction(2, 3))
    assert lv[(0, 0, 1)] == (Fraction(1, 3), Fraction(4, 3), Fraction(2, 3))
    assert directional_derivative(QUAD, third, third, third, (-1, 1, 0)) == (2, 0, 0)


def test_count():
    for n in range(8):
        assert len(indices(n)) == (n + 1) * (n + 2) // 2


def test_against_direct_sum_exact():
    rng = random.Random(61)
    for _ in range(150):
        n = rng.randint(0, 5)
        net = random_net(rng, n)
        r, s, t = random_bary(rng)
        assert triangle_point(net, r, s, t) == direct_sum(net, n, r, s, t)


def test_derivative_exact():
    rng = random.Random(62)
    for _ in range(80):
        n = rng.randint(1, 5)
        net = random_net(rng, n)
        r, s, t = random_bary(rng)
        d = (Fraction(rng.randint(-3, 3)), Fraction(rng.randint(-3, 3)))
        d = (d[0], d[1], -d[0] - d[1])
        assert directional_derivative(net, r, s, t, d) == direct_derivative(net, n, r, s, t, d)


def test_partition_of_unity_and_linear_precision():
    rng = random.Random(63)
    for n in range(1, 7):
        ones = {idx: (Fraction(1),) for idx in indices(n)}
        lin = from_function(n, lambda a, b, c: (a, b, c))
        for _ in range(10):
            r, s, t = random_bary(rng)
            assert triangle_point(ones, r, s, t) == (1,)
            assert triangle_point(lin, r, s, t) == (r, s, t)


def test_vertices_and_boundary():
    rng = random.Random(64)
    for _ in range(30):
        n = rng.randint(1, 5)
        net = random_net(rng, n)
        assert triangle_point(net, 1, 0, 0) == net[(n, 0, 0)]
        assert triangle_point(net, 0, 0, 1) == net[(0, 0, n)]
        a = Fraction(rng.randint(0, 12), 12)
        # side t = 0: the curve from the r vertex (a = 0) to the s vertex (a = 1)
        assert triangle_point(net, 1 - a, a, 0) == curve_sum(boundary_curve(net, 2), a)
        assert triangle_point(net, 0, 1 - a, a) == curve_sum(boundary_curve(net, 0), a)


def test_convex_hull_box():
    rng = random.Random(65)
    for _ in range(40):
        net = random_net(rng, rng.randint(1, 5))
        p = triangle_point(net, *random_bary(rng))
        for a in range(3):
            assert min(q[a] for q in net.values()) <= p[a] <= max(q[a] for q in net.values())


def test_bad_input():
    with pytest.raises(ValueError):
        triangle_point({(1, 0, 0): (0,), (0, 1, 0): (1,)}, 1, 0, 0)
    with pytest.raises(ValueError):
        directional_derivative(QUAD, 1, 0, 0, (1, 0, 0))
